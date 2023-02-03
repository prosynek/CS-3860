#!/usr/bin/python

'''
    Name : Paige Rosynek
    Course : CS 3860 041
    Lab 05 : Problem Solving with Data Analysis
    Date : 10.20.2022
'''


from cgi import test
import mysql.connector
import pandas as pd
import numpy as np



'''
    Establishes mySQL connection to stock_analytics database
    return : mySQL connection
'''
def start_connection():
    try:
        # TODO : set mysql password
        password = 'thisis4DB!01'
        connection = mysql.connector.connect(user='root', password=password, host='127.0.0.1', database='stock_analytics')
    except:
        print('password is incorrect')
    
    return connection


# loads all records from portfolio table
'''
    Loads all records from portfolio table into Pandas Dataframe
    return : Dataframe containing portfolio table
'''
def load_portfolio(connection):
    sql_query = ('SELECT * FROM portfolio')

    try:
        portfolio = pd.read_sql(sql_query, connection)
        portfolio['date'] = portfolio['date'].astype(str)   # convert date to string format
        
    except:
        raise Exception('error loading portfolio table')

    return portfolio



'''
    Verifies stock symbols are valid
    raise ValueError : if stock symbols don't match ['GOOG', 'CELG', 'NVDA', 'FB'] in order
'''
def verify_valid_stock_sym(syms):
    valid = ['GOOG', 'CELG', 'NVDA', 'FB']
    syms = [s.upper() for s in syms]

    if syms != valid:
        raise ValueError('invalid stock symbol(s)')
    

'''
    Verifies stock allocations sums to 1.0
    raise ValueError : if stock allocation doesn't sum to 1.0
'''
def verify_allocation(alloc):
    if round(sum(alloc), 1) != 1.0 and len(alloc) == 4:
        raise ValueError('allocation must include 4 weights & portfolio allocation must total to 1.0')


'''
    Calculates portfolio cumulative return 
    df : Dataframe of portfolio table
    alloc : list of portfolio allocation weights
'''
def calculate_portfolio_cum_return(df, alloc):
    # weighted average
    df['portfolio_cumulative_return'] = (df['GOOG_cumulative_return'] * alloc[0] + 
                                            df['CELG_cumulative_return'] * alloc[1] + 
                                            df['NVDA_cumulative_return'] * alloc[2] +
                                            df['FB_cumulative_return'] * alloc[3]) / sum(alloc)
    

'''
    Calculate daily stock value for each stock
    df : Dataframe of portfolio table
    stock_syms : list of stock symbols
    alloc : list of portfolio allocation weights
'''
def calc_stock_daily_values(df, stock_syms, alloc):
    # assume total portfolio value = $1
    for sym, loc in zip(stock_syms, alloc):
        df[f'{sym}_value'] = loc * 1.0 * df[f'{sym}_cumulative_return']

    # SPY value - assume value of $1
    df['SPY_value'] = 1.0 * df['SPY_cumulative_return']


'''
    Calculate portfolio value for each date
    df : Dataframe of portfolio table
    stock_syms : list of stock symbols
'''
def calc_portfolio_daily_values(df, stock_syms):
    # list of stock value column labels to use for filtering
    stock_val_labels = list()
    for sym in stock_syms:
        stock_val_labels.append(f'{sym}_value')

    df['portfolio_value'] = df[stock_val_labels].sum(axis=1)


'''
    Calculates the sharpe ratio of the portfolio for the entire table (all dates)
    df : Dataframe of portfolio table
'''
def sharpe_ratio(df):
    n = df['date'].count()
    r_a = df['portfolio_value']
    r_b = df['SPY_cumulative_return']
    std_daily_ret = np.std(r_a - r_b, axis=0)
    avg_daily_ret = np.mean(r_a - r_b)
    return std_daily_ret, avg_daily_ret, np.divide(np.sqrt(n) * avg_daily_ret, std_daily_ret)


'''
    Calculates the overall cumulative return for the portfolio
    df : Dataframe of portfolio table
'''
def calc_overall_portfolio_return(df):
    return (df['portfolio_value'].iloc[-1] - df['portfolio_value'].iloc[0]) / df['portfolio_value'].iloc[0]
    

'''
    Updates all the values of a single column in the portfolio table
    cursor : mySQL active cursor
    portfolio_df : Dataframe of portfolio table
    col_name : name of column to update in portfolio table
'''
def sql_update_col(cursor, portfolio_df, col_name):
    data = list(portfolio_df[[col_name, 'date']].apply(tuple, axis=1))
    query = f'UPDATE portfolio SET {col_name}=%s WHERE date=%s'
    cursor.executemany(query, data)



'''
    Executes sql update queries for the calculated columns
    connection : mySQL active connection
    stock_syms : list of stock symbols
    portfolio_df : Dataframe of portfolio table
'''
def sql_update(connection, stock_syms, portfolio_df):
    cursor = connection.cursor()

    # list of columns to update in portfolio table
    col_update = ['portfolio_value', 'portfolio_cumulative_return', 'SPY_value']
    for sym in stock_syms:
        col_update.append(f'{sym}_value')

    for col in col_update:
        print(f'updating {col} in portfolio table...')
        sql_update_col(cursor, portfolio_df, col)
    
    connection.commit()


# simulation function
'''
    Simulation function to calculate and update the portfolio table for 
    stock daily values, portfolio daily value, and portfolio cumulative return.
    Also calculates the sharpe value of the portfolio.
    stock_syms : list of stock symbols
    portfolio_alloc : list of portfolio allocation weights
    update_table : whether or not to commit update queries to database
    return : standard deviation of portfolio values, 
             average daily portfolio value, 
             sharpe ratio, 
             overall cumulative return of portfolio
'''
def run_simulation(stock_syms, portfolio_alloc, update_table=False):
    try:
        connection = start_connection()
        portfolio = load_portfolio(connection)  # dataframe 250x18

        # verify programmer input
        verify_valid_stock_sym(stock_syms)
        verify_allocation(portfolio_alloc)

        # calculate & update table
        calculate_portfolio_cum_return(portfolio, portfolio_alloc)
        calc_stock_daily_values(portfolio, stock_syms, portfolio_alloc)
        calc_portfolio_daily_values(portfolio, stock_syms)
        
        # update portfolio table
        if update_table:
            sql_update(connection, stock_syms, portfolio)
        connection.close()

        std_daily, avg_daily, sharpe = sharpe_ratio(portfolio)
        overall_return = calc_overall_portfolio_return(portfolio)

        portfolio.to_csv('./lab5 results/weights_max_sharpe.csv')

        return std_daily, avg_daily, sharpe, overall_return
        
    except (ValueError, Exception) as e:
        print(e)


'''
    Outputs simulation function results
'''
def print_results(syms, alloc, std_daily, avg_daily, sharpe, overall_return):
    print('stocks : \t', syms)
    print('allocation : \t', alloc)
    print()
    print(f'standard deviation portfolio daily return = {std_daily : >20}')
    print(f'average portfolio daily return = {avg_daily : >32}')
    print(f'portfolio overall culmulative return = {overall_return : >25}')
    print(f'sharpe ratio = {sharpe : >48}')


'''
    Finds the optimal weights that maximizes the sharpe value
    stock_syms : list of stock symbols
    return : maximum sharpe value, weights used to acheive maximum sharpr value
'''
def optimize_weights(stock_syms):
    val_range = np.around(np.arange(0, 1.1, 0.1), decimals=1).tolist()
    test_weights = []
    for x in val_range:
        for y in val_range:
            for k in val_range:
                for i in val_range:
                    l = [x,y,k,i]
                    if round(sum(l), 1) == 1.0:
                        test_weights.append(l)

    max_sharpe = 0.0
    max_weights = []
    for weights in test_weights:
        s, a, sharpe, o = run_simulation(stock_syms, weights)
        if sharpe > max_sharpe:
            max_sharpe = sharpe
            max_weights = weights
    
    return max_sharpe, max_weights


'''
    Main function. Runs simulation.
'''
if __name__ == '__main__':
    #----------SIMULATION INPUT----------
    stock_symbols = ['GOOG', 'CELG', 'NVDA', 'FB']
    stock_allocation = [0.3, 0.3, 0.2, 0.2]

    # better sharpe ratio
    # stock_allocation = [0.25, 0.25, 0.4, 0.1]

    # run simulation
    std_daily, avg_daily, sharpe, overall_return = run_simulation(stock_symbols, stock_allocation)
    print_results(stock_symbols, stock_allocation, std_daily, avg_daily, sharpe, overall_return)
    
    # find optimal sharpe value & weights
    max_sharpe, max_alloc = optimize_weights(stock_symbols)
    std_daily, avg_daily, sharpe, overall_return = run_simulation(stock_symbols, max_alloc, True)
    print_results(stock_symbols, max_alloc, std_daily, avg_daily, sharpe, overall_return)
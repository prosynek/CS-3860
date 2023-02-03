mysql.exe -uroot -p
thisis4DB!01

CREATE DATABASE stock_analytics;

USE stock_analytics;

# set global so you can read local files
SET GLOBAL local_infile=1;

//-- SPY table --
drop table IF EXISTS spy;

create table spy(
date date,	 
open float,	
high float,	
low float,
close float,	
volume float
);

load data local infile "C:/Users/rosynekp/OneDrive - Milwaukee School of Engineering/Desktop/cs 3860/labs/lab05/stock_data/spy_10042017.csv"
into table spy fields terminated by ',' lines terminated by '\n' ignore 1 lines
(@datevar, @openvar, @highvar, @lowvar, @closevar, volume)
SET date = STR_TO_DATE(@datevar, '%d-%M-%y'),
open = ROUND(@openvar, 2),
high = ROUND(@highvar, 2),  
low = ROUND(@lowvar, 2), 
close = ROUND(@closevar, 2);



show warnings;

select * from spy;

//-- GOOG table --
drop table IF EXISTS goog;
create table goog(
date date,	 
open float,	
high float,	
low float,
close float,	
volume float
);

load data local infile "C:/Users/rosynekp/OneDrive - Milwaukee School of Engineering/Desktop/cs 3860/labs/lab05/stock_data/goog_10042017.csv" 
into table goog fields terminated by ',' lines terminated by '\n' ignore 1 lines
(@datevar, @openvar, @highvar, @lowvar, @closevar, volume)
SET date = STR_TO_DATE(@datevar, '%d-%M-%y'),
open = ROUND(@openvar, 2),
high = ROUND(@highvar, 2),  
low = ROUND(@lowvar, 2), 
close = ROUND(@closevar, 2);

show warnings;

select * from goog;

//-- CELG table --
drop table if exists celg;
create table celg(
date date,
open float,	
high float,
low float,
close float,	
volume float
);

load data local infile "C:/Users/rosynekp/OneDrive - Milwaukee School of Engineering/Desktop/cs 3860/labs/lab05/stock_data/celg_10042017.csv" 
into table celg fields terminated by ',' lines terminated by '\n' ignore 1 lines
(@datevar, @openvar, @highvar, @lowvar, @closevar, volume)
SET date = STR_TO_DATE(@datevar, '%d-%M-%y'),
open = ROUND(@openvar, 2),
high = ROUND(@highvar, 2),  
low = ROUND(@lowvar, 2), 
close = ROUND(@closevar, 2);

show warnings;

select * from celg;

//-- NVDA table --
drop table IF EXISTS nvda;
create table nvda(
date date,
open float,
high float,
low float,
close float,	
volume float
);

load data local infile "C:/Users/rosynekp/OneDrive - Milwaukee School of Engineering/Desktop/cs 3860/labs/lab05/stock_data/nvda_10042017.csv" 
into table nvda fields terminated by ',' lines terminated by '\n' ignore 1 lines
(@datevar, @openvar, @highvar, @lowvar, @closevar, volume)
SET date = STR_TO_DATE(@datevar, '%d-%M-%y'),
open = ROUND(@openvar, 2),
high = ROUND(@highvar, 2),  
low = ROUND(@lowvar, 2), 
close = ROUND(@closevar, 2);

show warnings;

select * from nvda;

//-- FB table --
drop table IF EXISTS fb;
create table fb(
date date,
open float,
high float,
low float,
close float,	
volume float
);

load data local infile "C:/Users/rosynekp/OneDrive - Milwaukee School of Engineering/Desktop/cs 3860/labs/lab05/stock_data/fb_10042017.csv" 
into table fb fields terminated by ',' lines terminated by '\n' ignore 1 lines
(@datevar, @openvar, @highvar, @lowvar, @closevar, volume)
SET date = STR_TO_DATE(@datevar, '%d-%M-%y'),
open = ROUND(@openvar, 2),
high = ROUND(@highvar, 2),  
low = ROUND(@lowvar, 2), 
close = ROUND(@closevar, 2);

show warnings;

select * from fb;

//-- portfolio table --

(Date,
S1 Adjusted Close, S1 Cumulative Return, S1 Value,
S2 Adjusted Close, S2 Cumulative Return, S2 Value,
S3 Adjusted Close, S3 Cumulative Return, S3 Value,
S4 Adjusted Close, S4 Cumulative Return, S4 Value,
SPY Adjusted Close, SPY Cumulative Return, SPY Value,
Portfolio Cumulative Return, Portfolio Value)

CREATE TABLE portfolio (
date DATE,
CELG_adjusted_close FLOAT,
CELG_cumulative_return FLOAT,
CELG_value FLOAT,
FB_adjusted_close FLOAT,
FB_cumulative_return FLOAT,
FB_value FLOAT,
GOOG_adjusted_close FLOAT,
GOOG_cumulative_return FLOAT,
GOOG_value FLOAT,
NVDA_adjusted_close FLOAT,
NVDA_cumulative_return FLOAT,
NVDA_value FLOAT,
SPY_adjusted_close FLOAT,
SPY_cumulative_return FLOAT,
SPY_value FLOAT,
portfolio_cumulative_return FLOAT,
portfolio_value FLOAT
);

INSERT INTO portfolio (date, CELG_adjusted_close, FB_adjusted_close, GOOG_adjusted_close, NVDA_adjusted_close, SPY_adjusted_close)
SELECT celg.date, celg.close, fb.close, goog.close, nvda.close, spy.close
FROM celg, fb, goog, nvda, spy
WHERE celg.date = fb.date AND fb.date = goog.date AND goog.date = nvda.date AND nvda.date = spy.date
ORDER BY celg.date ASC;

//-- calculate cumulative return --
UPDATE portfolio p1, portfolio p2
SET p1.CELG_cumulative_return = p1.CELG_adjusted_close / (
    SELECT p2.CELG_adjusted_close 
    WHERE p2.date='2016-10-06'
);

UPDATE portfolio p1, portfolio p2
SET p1.FB_cumulative_return = p1.FB_adjusted_close / (
    SELECT p2.FB_adjusted_close 
    WHERE p2.date='2016-10-06'
);

UPDATE portfolio p1, portfolio p2
SET p1.GOOG_cumulative_return = p1.GOOG_adjusted_close / (
    SELECT p2.GOOG_adjusted_close 
    WHERE p2.date='2016-10-06'
);

UPDATE portfolio p1, portfolio p2
SET p1.NVDA_cumulative_return = p1.NVDA_adjusted_close / (
    SELECT p2.NVDA_adjusted_close 
    WHERE p2.date='2016-10-06'
);

UPDATE portfolio p1, portfolio p2
SET p1.SPY_cumulative_return = p1.SPY_adjusted_close / (
    SELECT p2.SPY_adjusted_close 
    WHERE p2.date='2016-10-06'
);


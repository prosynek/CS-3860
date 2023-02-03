"""
- CS3860 041
- Fall 2022
- Final Project - MongoDB
- Name: Paige Rosynek
- Date: 11.11.2022
"""
import pymongo
import pandas as pd
from pymongo import MongoClient


Q3 = '3. List the number of videos for each video category.'
Q4 = '4. List the number of videos for each video category where the inventory is non-zero.'
Q5 = '5. For each actor, list the video categories that actor has appeared in.'
Q6 = '6. Which actors have appeared in movies in different video categories?'
Q7 = '7. Which actors have not appeared in a comedy?'
Q8 = '8. Which actors have appeared in both a comedy and an action adventure movie?'


# FIELDS = ["recording_id", "title", "director", "category", "actors", "image_name", "duration", "rating", "year_released", "price", "stock_count"]

def connect_to_client():
    """
    Connects to MongoDB client
    
    Returns:
        client: MongoDB client connected to Atlas cluster
    """
    client = pymongo.MongoClient("mongodb+srv://root:passthesoup@cluster0.ob1knen.mongodb.net/?retryWrites=true&w=majority")
    return client


def question_3(collection):
    """
    Lists the number of films for each category in the collection.
    Answers question 3: List the number of videos for each video category.

    Args:
        collection: MongoDB collection obj (films)

    Returns:
        category_dict: dictionary containing each category as keys and count as value {'category' : count, ...}
    """
    category_dict = {}  # {category : count, ...}
    
    # loop through each document in collection
    for document in collection.find():
        category = document['category']
        
        # if key doesnt exist
        if not category in category_dict:
            category_dict[category] = 0
        
        category_dict[category] += 1

    return category_dict


def question_4(collection):
    """
    Lists the number of films for each category in the collection where the inventory is nonzero.
    Answers question 4: List the number of videos for each video category where the inventory is non-zero.
    
    Args:
        collection: MongoDB collection obj (films)

    Returns:
        category_dict: dictionary containing each category as keys and count as value {'category' : count, ...}
    """
    category_dict = {}  # {category : count, ...}
    
    # loop through each document in collection
    for document in collection.find():
        category = document['category']
        
        # if key doesnt exist
        if not category in category_dict:
            category_dict[category] = 0
        
        if document['stock_count'] > 0: 
            category_dict[category] += 1

    return category_dict

 
def question_5(collection):
    """
    Lists the categories each actor has appeared in.
    Answers question 5: For each actor, list the video categories that actor has appeared in.
    
    Args:
        collection: MongoDB collection obj (films)

    Returns:
        actor_dict: dictionary such {'actorname' : [category1, category2], 'actorname' : [category3],...}
    """
    actor_dict = {}
    
    # loop through each document in collection
    for document in collection.find():
        actors = document['actors']
        
        for actor in actors:
            if not actor in actor_dict:
                actor_dict[actor] = []
            
            # if film category not already listed for actor
            if not document['category'] in actor_dict[actor]:
                actor_dict[actor].append(document['category'])
        
    return actor_dict


def question_6(collection):
    """
    Lists the categories each actor has appeared in if they appeared in more than 1 category.
    Answers question 6: Which actors have appeared in movies in different video categories?
    
    Args:
        collection: MongoDB collection obj (films)

    Returns:
        diff_categories: dictionary such {'actorname' : [category1, category2],...}
    """
    actor_category = question_5(collection)
    diff_categories = {}
    
    for key, value in actor_category.items():
        if len(value) > 1:
            diff_categories[key] = value
    
    return diff_categories

 
def question_7(collection):
    """
    Lists the actors that have not appeared in a comedy.
    Answers question 7: Which actors have not appeared in a comedy?

    Args:
        collection: MongoDB collection obj (films)

    Returns:
        actors: list of actor names of actors that have not appeared in a comedy
    """
    actor_category = question_5(collection)
    actors = []
    
    for key, value in actor_category.items():
        if not 'Comedy' in value:
            actors.append(key)
    
    return actors


def question_8(collection):
    """
    Lists the actors that have appeared in both a comedy and action adventure film.
    Answers question 8: Which actors have appeared in both a comedy and an action adventure movie?

    Args:
        collection: MongoDB collection obj (films)

    Returns:
        actors: list of actor names of actors that appeared in both a comedy and action adventure film
    """
    actor_category = question_5(collection)
    actors = []
    
    for key, value in actor_category.items():
        if ('Comedy' in value) and ('Action & Adventure' in value):
            actors.append(key)

    return actors

    
def answer_questions(collection):
    """
    Runs the queries for questions 3-8

    Args:
        collection: MongoDB collection obj (films)
    """
    # QUESTION 3
    q3 = question_3(collection)
    print(f'{Q3}\n\n{q3}\n({len(q3)} results)\n')

    # QUESTION 4
    q4 = question_4(collection)
    print(f'{Q4}\n\n{q4}\n({len(q4)} results)\n')
    
    # QUESTION 5
    q5 = question_5(collection)
    print(f'{Q5}\n\n{q5}\n({len(q5)} results)\n')
    
    # QUESTION 6
    q6 = question_6(collection)
    print(f'{Q6}\n\n{q6}\n({len(q6)} results)\n')
    
    # QUESTION 7
    q7 = question_7(collection)
    print(f'{Q7}\n\n{q7}\n({len(q7)} results)\n')

    # QUESTION 8
    q8 = question_8(collection)
    print(f'{Q8}\n\n{q8}\n({len(q8)} results)\n')


if __name__ == '__main__':
    client = connect_to_client()
    database = client['final_project']
    collection = database['films']
    answer_questions(collection)
    
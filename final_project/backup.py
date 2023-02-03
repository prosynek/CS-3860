import pymongo
import pandas as pd

from pymongo import MongoClient


Q3 = '3. List the number of videos for each video category.'
Q4 = '4. List the number of videos for each video category where the inventory is non-zero.'
Q5 = '5. For each actor, list the video categories that actor has appeared in.'
Q6 = '6. Which actors have appeared in movies in different video categories?'
Q7 = '7. Which actors have not appeared in a comedy?'
Q8 = '8. Which actors have appeared in both a comedy and an action adventure movie?'


FIELDS = ["recording_id", "title", "director", "category", "actors", "image_name", "duration", "rating", "year_released", "price", "stock_count"]

def connect_to_client():
    client = pymongo.MongoClient("mongodb+srv://root:passthesoup@cluster0.ob1knen.mongodb.net/?retryWrites=true&w=majority")
    return client

# 3. List the number of videos for each video category.
def question_3(collection):
    category_dict = {}  # {category : count, ...}
    
    # loop through each document in collection
    for document in collection.find():
        category = document['category']
        
        # if key doesnt exist
        if not category in category_dict:
            category_dict[category] = 0
        
        category_dict[category] += 1

    return category_dict

# 4. List the number of videos for each video category where the inventory is non-zero.
def question_4(collection):
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


# 5. For each actor, list the video categories that actor has appeared in.
def question_5(collection):
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


# 6. Which actors have appeared in movies in different video categories?
def question_6(collection):
    actor_category = question_5(collection)
    diff_categories = {}
    
    for key, value in actor_category.items():
        if len(value) > 1:
            diff_categories[key] = value
    
    return diff_categories


# 7. Which actors have not appeared in a comedy?
def question_7(collection):
    actor_category = question_5(collection)
    actors = []
    
    for key, value in actor_category.items():
        if not 'Comedy' in value:
            actors.append(key)
    
    return actors


# 8. Which actors have appeared in both a comedy and an action adventure movie?
def question_8(collection):
    actor_category = question_5(collection)
    actors = []
    
    for key, value in actor_category.items():
        if ('Comedy' in value) and ('Action & Adventure' in value):
            actors.append(key)

    return actors

    
# TODO : output number of results for each question
def answer_questions(collection):
    # QUESTION 3
    print(f'{Q3}\n{question_3(collection)}\n')

    # QUESTION 4
    print(f'{Q4}\n{question_4(collection)}\n')
    
    # QUESTION 5
    print(f'{Q5}\n{question_5(collection)}\n')
    
    # QUESTION 6
    print(f'{Q6}\n{question_6(collection)}\n')
    
    # QUESTION 7
    print(f'{Q7}\n{question_7(collection)}\n')

    # QUESTION 8
    print(f'{Q8}\n{question_8(collection)}\n')


if __name__ == '__main__':
    client = connect_to_client()
    database = client['final_project']
    collection = database['films']
    answer_questions(collection)
    
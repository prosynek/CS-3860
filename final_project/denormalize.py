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

COLLECTIONS = ['video_recordings', 'categories', 'video_actors']
FIELDS = ["title", "director", "category", "actors", "image_name", "duration", "rating", "year_released", "price", "stock_count"] # _id


def connect_to_client():
    """
    Connects to MongoDB client
    
    Returns:
        client: MongoDB client connected to Atlas cluster
    """
    client = pymongo.MongoClient("mongodb+srv://root:passthesoup@cluster0.ob1knen.mongodb.net/?retryWrites=true&w=majority")
    return client


def get_actors_recording_id(database, rec_id):
    """
    Lists all the actors for a specified recording_id (film)
    
    Args:
        database: MongoDB database obj
        rec_id: int, recording_id to find the actors for
    Returns:
        actor_list: list of actor names of actors for the specified recording_id
    """
    actor_list = []
    video_actors = database[COLLECTIONS[2]]
    
    # get documents where recording_id = rec_id
    query = {'recording_id' : rec_id}
    actors = video_actors.find(query, {'_id' : 0, 'name' : 1})  # return only the name field
    
    # stores actors names
    for actor in actors: 
        if not actor['name'] in actor_list:
            actor_list.append(actor['name'])

    return actor_list


def format_insert_query(dictionary):
    """
    Formats the insert query to insert denormalized data into a collection

    Args:
        dictionary: dictionary, contains all the denomalized data for each record

    Returns:
        query: dictionary, formatted query to insert data into a collection
    """
    query = []

    for key in dictionary.keys():
        temp_d = {}
        temp_d['recording_id'] = key
    
        for i in range(len(FIELDS)):
            temp_d[FIELDS[i]] = dictionary[key][i]
            
        query.append(temp_d)

    return query


def get_fields_list(database, recording_id, document):
    """
    Gets all the field values for a specified recording_id

    Args:
        database: MonogoDB database obj
        recording_id: int, recording_id to find the field values for
        document: MongoDB document obj to get the field values from

    Returns:
        field_values: list of field values for a specific recording_id
    """
    field_values = []
    
    for field in FIELDS:
        if field == 'actors':
            field_values.append(get_actors_recording_id(database, recording_id))
        else:
            field_values.append(document[field])
            
    return field_values
    

def get_data_dictionary(client, database):
    """
    Creates a dictionary of all the distinct films in the database

    Args:
        client: MongoDB client obj
        database: MongoDB database obj to get data from

    Returns:
        dictionary: dictionary of all the distinct data, such {recording_id : ['title', 'director',...]}
    """
    dictionary = {}
    video_recordings = database[COLLECTIONS[0]]
    documents = video_recordings.find()
    
    # type(doc) => dict
    for doc in documents:
        recording_id = doc['recording_id']

        # if recording id doesnt exist as key already => add 
        if not recording_id in dictionary:
            dictionary[recording_id] = get_fields_list(database, recording_id, doc)

    return dictionary
       
       
def create_denormalized_collection(database, query):
    """
    Creates a collection from the denomalized data

    Args:
        database: MongoDB client obj
        query: dictionary that represents the insert query

    Returns:
        collection: MongoDB collection obj of the created collection
    """
    collection = database['films']
    collection.insert_many(query)
    return collection


def denormalize(client, database):
    """
    Denormalizes relational tables into NoSQL collection

    Args:
        client: MongoDB client obj
        database: MongoDB database obj 
    """     
    dictionary = get_data_dictionary(client, database)
    query = format_insert_query(dictionary)
    collection = create_denormalized_collection(database, query)
    for doc in collection:
        print(doc)
        
        
if __name__ == '__main__':
    client = connect_to_client()
    database = client['final_project']
    denormalize(client, database)
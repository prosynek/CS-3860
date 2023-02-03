import pymongo

from pymongo import MongoClient
client = pymongo.MongoClient("mongodb+srv://root:passthesoup@cluster0.ob1knen.mongodb.net/?retryWrites=true&w=majority")

databases = client.list_database_names()

for db in databases:
    print(db)
    print(client[db].list_collection_names())

'''
for coll in database.list_collection_names():
    print(coll)
    collection = database[coll]
    print(collection)
    for x in collection.find():
        print(x)
'''
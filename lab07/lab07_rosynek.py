# followed the tutorial : https://realpython.com/introduction-to-mongodb-and-python/
import pymongo

from pymongo import MongoClient
client = MongoClient('mongodb+srv://root:passthesoup@cluster0.yqdrovh.mongodb.net/cs3860_lab07')

db = client['cs3860_lab07']
print(db)

for coll in db.list_collection_names():
    print(coll)
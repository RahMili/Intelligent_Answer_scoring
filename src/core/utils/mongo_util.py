from pymongo import MongoClient

client = MongoClient()


def connect_collection(db, col):
    db_client = MongoClient("mongodb://127.0.0.1:27017/")
    db = db_client[db]
    col = db[col]
    return db, col

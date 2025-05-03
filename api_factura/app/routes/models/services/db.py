from pymongo import MongoClient
from app.config import MONGO_URI, DB_NAME

def get_database():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]
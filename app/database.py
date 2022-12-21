from pymongo import MongoClient
import pymongo
from app.config import settings
def dbconnection():
    client = MongoClient(settings.DATABASE_URL)
    print('Connected to MongoDB...')
    db = client[settings.MONGO_INITDB_DATABASE]
    return db

User = dbconnection().users
User.create_index([("email", pymongo.ASCENDING)], unique=True)
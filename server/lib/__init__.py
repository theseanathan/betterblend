from pymongo import MongoClient

from server import settings

client = MongoClient('localhost', 27017)
mongo_db = client[settings.DB]

tokens_collection = mongo_db[settings.TOKENS_COLLECTION]

from pymongo import MongoClient
import config


client = MongoClient(config.DATABASE_URI)
users  = client.stutern69.users

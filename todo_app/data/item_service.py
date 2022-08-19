import os
import pymongo

class ItemService:
    def __init__(self):
        connection_string = os.getenv("CONNECTION_STRING")
        database_name = os.getenv("DATABASE_NAME")
        client = pymongo.MongoClient(connection_string)
        self.db = client[database_name]
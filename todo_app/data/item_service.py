import os
import pymongo

from todo_app.models.Card import Card

class ItemService:
    def __init__(self):
        connection_string = os.getenv("CONNECTION_STRING")
        database_name = os.getenv("DATABASE_NAME")
        client = pymongo.MongoClient(connection_string)
        self.db = client[database_name]
    
    def get_items(self):
        return [ Card.from_database(item) for item in self.db['todo-items'].find()]
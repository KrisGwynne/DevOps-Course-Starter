import os
import pymongo

from todo_app.models.Card import Card

class ItemService:
    def __init__(self):
        connection_string = os.getenv("CONNECTION_STRING")
        database_name = os.getenv("DATABASE_NAME")
        client = pymongo.MongoClient(connection_string)
        self.db = client[database_name]
        self.item_collection = self.db['todo-items']
    
    def get_items(self):
        return [ Card.from_database(item) for item in self.item_collection.find()]

    def add_item(self, title):
        new_item = {
            "title": title,
            "status": "To Do"
        }
        self.item_collection.insert_one(new_item)

    def start_item(self, id):
        self.__update_item_status(id, "Doing")

    def complete_item(self, id):
        self.__update_item_status(id, "Done")

    def delete_item(self, id):
        self.item_collection.delete_one({ "_id": id })
        
    def __update_item_status(self, id, status):
        self.item_collection.update_one({ "_id": id }, { "$set": { "status": status }})
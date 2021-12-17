from typing import List
from todo_app.models.Card import Card

class ItemViewModel:
    def __init__(self, items: List[Card]) -> None:
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        return [item for item in self._items if item.status == "To Do"]
        return self._items

    @property
    def doing_items(self):
        return [item for item in self._items if item.status == "Doing"]
    
    @property
    def done_items(self):
        return [item for item in self._items if item.status == "Done"]
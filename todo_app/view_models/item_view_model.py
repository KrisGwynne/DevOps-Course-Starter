from typing import List
from todo_app.models.Card import Card

class ItemViewModel:
    def __init__(self, items: List[Card], user_role) -> None:
        self._items = items
        self._can_edit = user_role == "writer"

    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        return [item for item in self._items if item.status == "To Do"]

    @property
    def doing_items(self):
        return [item for item in self._items if item.status == "Doing"]
    
    @property
    def done_items(self):
        return [item for item in self._items if item.status == "Done"]

    @property
    def can_edit(self):
        return self._can_edit
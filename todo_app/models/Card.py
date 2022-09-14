class Card:
    def __init__(self, id, title, status):
        self.id = id
        self.title = title
        self.status = status

    @classmethod
    def from_database(cls, item):
        return cls(item['_id'], item['title'], item['status'])

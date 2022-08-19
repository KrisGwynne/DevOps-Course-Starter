class Card:
    def __init__(self, id, title, status):
        self.id = id
        self.title = title
        self.status = status

    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card['id'], card['name'], list['name'])

    @classmethod
    def from_database(cls, item):
        return cls(item['_id'], item['title'], item['status'])

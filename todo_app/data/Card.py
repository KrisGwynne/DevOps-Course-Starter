class Card:
    def __init__(self, trello_card, list_name):
        self.id = trello_card["id"]
        self.title = trello_card["name"]
        self.status = "Completed" if list_name == "Done" else "Not Started"
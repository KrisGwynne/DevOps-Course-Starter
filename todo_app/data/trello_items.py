import os
import requests
from todo_app.data.Card import Card

_BASE_URL = "https://api.trello.com"

_API_QUERY_PARAMS = {'key': os.getenv("API_KEY"), 'token': os.getenv("API_TOKEN")}

def get_items():
    params = _API_QUERY_PARAMS | {'cards': 'open'}
    # TODO: Handle bad api response
    res = requests.get(f'{_BASE_URL}/1/boards/{os.getenv("BOARD_ID")}/lists', params=params)
    return [Card(card, list['name']) for list in res.json() for card in list['cards']]

def add_item(title):
    # Get the To-Do list id
    # TODO: handle api failure
    res = requests.get(f'{_BASE_URL}/1/boards/{os.getenv("BOARD_ID")}/lists', params=_API_QUERY_PARAMS)
    list_id = next(list for list in res.json() if list['name'] == "To Do")["id"]
    
    # Add card to the To-Do list
    params = _API_QUERY_PARAMS | {'name': title, 'idList': list_id}
    # TODO: handle api failure
    requests.post(f'{_BASE_URL}/1/cards', params=params)
    
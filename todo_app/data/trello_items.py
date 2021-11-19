import os
import requests
from todo_app.data.Card import Card

_BASE_URL = "https://api.trello.com"

_API_QUERY_PARAMS = {'key': os.getenv("API_KEY"), 'token': os.getenv("API_TOKEN")}

def get_items():
    params = _API_QUERY_PARAMS | {'cards': 'open'}
    # TODO: Handle bad api response
    res = requests.get(f'{_BASE_URL}/1/boards/{os.getenv("BOARD_ID")}/lists', params=params)
    return [Card.from_trello_card(card, list) for list in res.json() for card in list['cards']]

def add_item(title):
    # Get the To-Do list id
    list_id = get_list_id('To Do')
    
    # Add card to the To-Do list
    params = _API_QUERY_PARAMS | {'name': title, 'idList': list_id}
    # TODO: handle api failure
    requests.post(f'{_BASE_URL}/1/cards', params=params)

def complete_item(id):
    # Get the Done list id
    list_id = get_list_id('Done')

    # Move card to Done list
    params = _API_QUERY_PARAMS | {'idList': list_id}
    requests.put(f'{_BASE_URL}/1/cards/{id}', params=params)


def get_list_id(list_name):
    # TODO: handle api failure
    res = requests.get(f'{_BASE_URL}/1/boards/{os.getenv("BOARD_ID")}/lists', params=_API_QUERY_PARAMS)
    return next(list for list in res.json() if list['name'] == list_name)["id"]
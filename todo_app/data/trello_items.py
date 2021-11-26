import os
import requests
from todo_app.models.ApiException import ApiException
from todo_app.models.Card import Card

_BASE_URL = "https://api.trello.com"

_API_QUERY_PARAMS = {'key': os.getenv("API_KEY"), 'token': os.getenv("API_TOKEN")}

def get_items():
    params = _API_QUERY_PARAMS | {'cards': 'open'}
    res = requests.get(f'{_BASE_URL}/1/boards/{os.getenv("BOARD_ID")}/lists', params=params)

    if not res.ok:
        raise ApiException("Error getting to-do items")

    return [Card.from_trello_card(card, list) for list in res.json() for card in list['cards']]

def add_item(title):
    # Get the To-Do list id
    list_id = get_list_id('To Do')
    
    # Add card to the To-Do list
    params = _API_QUERY_PARAMS | {'name': title, 'idList': list_id}
    res = requests.post(f'{_BASE_URL}/1/cards', params=params)

    if not res.ok:
        raise ApiException("Error adding a new to-do item")

def complete_item(id):
    # Get the Done list id
    list_id = get_list_id('Done')

    # Move card to Done list
    params = _API_QUERY_PARAMS | {'idList': list_id}
    res = requests.put(f'{_BASE_URL}/1/cards/{id}', params=params)

    if not res.ok:
        raise ApiException("Error completing to-do item")

def delete_item(id):
    res = requests.delete(f'{_BASE_URL}/1/cards/{id}', params=_API_QUERY_PARAMS)

    if not res.ok:
        raise ApiException("Error deleting to-do item")


def get_list_id(list_name):
    res = requests.get(f'{_BASE_URL}/1/boards/{os.getenv("BOARD_ID")}/lists', params=_API_QUERY_PARAMS)

    if not res.ok:
        raise ApiException("Error getting to-do items")

    return next(list for list in res.json() if list['name'] == list_name)["id"]
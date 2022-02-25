import os
import requests
from todo_app.models.ApiException import ApiException
from todo_app.models.Card import Card

_BASE_URL = "https://api.trello.com"

def get_api_query_params():
    return {'key': os.getenv("API_KEY"), 'token': os.getenv("API_TOKEN")}

def get_items():
    params = {'cards': 'open'}
    params.update(get_api_query_params())
    res = requests.get(f'{_BASE_URL}/1/boards/{os.getenv("BOARD_ID")}/lists', params=params)

    if not res.ok:
        raise ApiException("Error getting to-do items")

    return [Card.from_trello_card(card, list) for list in res.json() for card in list['cards']]

def add_item(title):
    # Get the To-Do list id
    list_id = get_list_id('To Do')
    
    # Add card to the To-Do list
    params = {'name': title, 'idList': list_id}
    params.update(get_api_query_params())
    res = requests.post(f'{_BASE_URL}/1/cards', params=params)

    if not res.ok:
        raise ApiException("Error adding a new to-do item")

def start_item(id):
    list_id = get_list_id('Doing')

    params = {'idList': list_id}
    params.update(get_api_query_params())
    res = requests.put(f'{_BASE_URL}/1/cards/{id}', params=params)

    if not res.ok:
        raise ApiException('Error starting to-do item')

def complete_item(id):
    # Get the Done list id
    list_id = get_list_id('Done')

    # Move card to Done list
    params = {'idList': list_id}
    params.update(get_api_query_params())
    res = requests.put(f'{_BASE_URL}/1/cards/{id}', params=params)

    if not res.ok:
        raise ApiException("Error completing to-do item")

def delete_item(id):
    res = requests.delete(f'{_BASE_URL}/1/cards/{id}', params=get_api_query_params())

    if not res.ok:
        raise ApiException("Error deleting to-do item")


def get_list_id(list_name):
    res = requests.get(f'{_BASE_URL}/1/boards/{os.getenv("BOARD_ID")}/lists', params=get_api_query_params())

    if not res.ok:
        raise ApiException("Error getting to-do items")

    return next(list for list in res.json() if list['name'] == list_name)["id"]
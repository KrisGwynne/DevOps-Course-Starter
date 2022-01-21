import requests
import os
import pytest
from threading import Thread
from todo_app import app
from selenium import webdriver
from dotenv import load_dotenv, find_dotenv

from todo_app.models.ApiException import ApiException


def create_e2e_trello_board():
    _API_QUERY_PARAMS = {'key': os.environ.get("API_KEY"), 'token': os.environ.get("API_TOKEN")}
    board_name = 'e2e_board'
    organisation_id = os.environ.get("ORGANISATION_ID")
    params = _API_QUERY_PARAMS | {'name': board_name, 'idOrganization': organisation_id}
    res1 = requests.post('https://api.trello.com/1/boards', params=params)

    res = requests.get(f'https://api.trello.com/1/organizations/{organisation_id}/boards', params=_API_QUERY_PARAMS)

    if not res1.ok:
        raise ApiException(res1.status_code)

    return next(board['id'] for board in res.json() if board['name'] == board_name)

def delete_e2e_trello_board(id):
    _API_QUERY_PARAMS = {'key': os.environ.get("API_KEY"), 'token': os.environ.get("API_TOKEN")}
    requests.delete(f'https://api.trello.com/1/boards/{id}', params=_API_QUERY_PARAMS)

@pytest.fixture(scope='module')
def app_with_temp_board():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    # Create the new board & update the board id environment variable
    board_id = create_e2e_trello_board()
    os.environ['TRELLO_BOARD_ID'] = board_id
    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    # Tear Down
    thread.join(1)
    delete_e2e_trello_board(board_id)

@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

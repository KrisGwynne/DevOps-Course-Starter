from time import sleep
import os
import pytest
from threading import Thread
from todo_app import app
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from dotenv import load_dotenv, find_dotenv
import pymongo

def drop_e2e_database(database_name):
    client = pymongo.MongoClient(os.getenv('CONNECTION_STRING'))
    client.drop_database(database_name)

@pytest.fixture(scope='module')
def app_with_temp_board():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    # Mongo will create a new db for e2e tests when creating new documents
    e2e_database_name = 'todo-app-e2e'
    os.environ['DATABASE_NAME'] = e2e_database_name
    os.environ['LOGIN_DISABLED'] = 'True'
    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    # Ensure the application is running before running the tests
    sleep(1)
    yield application
    # Tear Down
    thread.join(1)
    drop_e2e_database(e2e_database_name)

@pytest.fixture(scope="module")
def driver():
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    with webdriver.Firefox(options=opts) as driver:
        driver.implicitly_wait(10)
        yield driver

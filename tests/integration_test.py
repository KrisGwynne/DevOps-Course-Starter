import os
import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app import app 
import mongomock
import pymongo

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        setup_mock_data()

        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def test_index_page(client):
    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == 200
    assert 'Test card' in response.data.decode()

def setup_mock_data():
    client = pymongo.MongoClient(os.getenv('CONNECTION_STRING'))
    db = client[os.getenv('DATABASE_NAME')]
    collection = db['todo-items']
    collection.insert_one({
        "title": "Test card",
        "status": "To Do"
    })
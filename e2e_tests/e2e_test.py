from setup import driver, app_with_temp_board
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class TestE2e:
    @staticmethod
    def test_app_title(driver, app_with_temp_board):
        driver.get('http://localhost:5000/')
        assert driver.title == 'To-Do App'

    @staticmethod
    def test_create_new_todo_item(driver: webdriver.Firefox, app_with_temp_board):
        print('starting test')
        driver.get('http://localhost:5000/')
        elem = driver.find_element(By.NAME, 'item_title')
        elem.clear()
        elem.send_keys("New Item 1")
        elem.send_keys(Keys.RETURN)
        assert driver.title == 'To-Do App'
        assert driver.find_element(By.XPATH, "//*[contains(text(), 'New Item 1')]")
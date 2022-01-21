from setup import driver, app_with_temp_board

class TestE2e:
    @staticmethod
    def test_task_journey(driver, app_with_temp_board):
        driver.get('http://localhost:5000/')
        assert driver.title == 'To-Do App'
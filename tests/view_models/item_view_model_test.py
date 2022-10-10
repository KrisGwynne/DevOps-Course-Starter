from todo_app.view_models.item_view_model import ItemViewModel
from todo_app.models.Card import Card

class TestItemViewModel:
    @staticmethod
    def test_getting_to_do_items_returns_only_to_do_items():
        # Arrange
        todo_item = Card(0, "title", "To Do")
        doing_item = Card(0, "title", "Doing")
        done_item = Card(1, "done", "Done")
        model = ItemViewModel([todo_item, doing_item, done_item], 'writer')

        # Act
        items = model.todo_items

        # Assert
        assert todo_item in items
        assert doing_item not in items
        assert done_item not in items

    @staticmethod
    def test_getting_to_do_items_when_empty_returns_empty_list():
        # Arrange
        model = ItemViewModel([], 'writer')

        # Act
        items = model.todo_items

        # Assert
        assert len(items) == 0

    @staticmethod
    def test_getting_doing_items_returns_only_doing_items():
        # Arrange
        todo_item = Card(0, "title", "To Do")
        doing_item = Card(0, "title", "Doing")
        done_item = Card(1, "done", "Done")
        model = ItemViewModel([todo_item, doing_item, done_item], 'writer')

        # Act
        items = model.doing_items

        # Assert
        assert todo_item not in items
        assert doing_item in items
        assert done_item not in items

    @staticmethod
    def test_getting_doing_items_when_empty_returns_empty_list():
        # Arrange
        model = ItemViewModel([], 'writer')

        # Act
        items = model.doing_items

        # Assert
        assert len(items) == 0

    @staticmethod
    def test_getting_done_items_returns_only_done_items():
        # Arrange
        todo_item = Card(0, "title", "To Do")
        doing_item = Card(0, "title", "Doing")
        done_item = Card(1, "done", "Done")
        model = ItemViewModel([todo_item, doing_item, done_item], 'writer')

        # Act
        items = model.done_items

        # Assert
        assert todo_item not in items
        assert doing_item not in items
        assert done_item in items

    @staticmethod
    def test_getting_done_items_when_empty_returns_empty_list():
        # Arrange
        model = ItemViewModel([], 'writer')

        # Act
        items = model.done_items

        # Assert
        assert len(items) == 0
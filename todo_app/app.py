from flask import Flask, redirect, render_template, request
from flask.helpers import flash
from todo_app.data.item_service import ItemService
from todo_app.flask_config import Config
from todo_app.models.ApiException import ApiException
from todo_app.view_models.item_view_model import ItemViewModel

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    itemService = ItemService()

    @app.route('/')
    def index():
        items = []
        try:
            items = itemService.get_items()
        except ApiException as err:
            flash(err.message, "error")

        sorted_items = sorted(items, key=lambda item: item.status, reverse=True)
        item_view_model = ItemViewModel(sorted_items)
        return render_template("index.html", view_model=item_view_model)

    @app.route('/item', methods=['POST'])
    def add_item():
        title = request.form.get("item_title")
        try:
            itemService.add_item(title)
            flash("Added new to-do item", "success")
        except ApiException as err:
            flash(err.message, "error")

        return redirect("/")

    @app.route('/items/<id>/start', methods=['POST'])
    def start_item(id):
        try:
            itemService.start_item(id)
            flash("Started to-do item", "success")
        except ApiException as err:
            flash(err.message, "error")

        return redirect('/')

    @app.route('/items/<id>/complete', methods=['POST'])
    def complete_item(id):
        try:
            itemService.complete_item(id)
            flash("Completed to-do item", "success")
        except ApiException as err:
            flash(err.message, "error")

        return redirect('/')

    @app.route('/items/delete/<id>', methods=['POST'])
    def delete_item(id):
        try:
            itemService.delete_item(id)
            flash("Deleted to-do item", "success")
        except ApiException as err:
            flash(err.message, "error")

        return redirect('/')
    
    return app

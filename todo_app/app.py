from flask import Flask, redirect, render_template, request
from flask.helpers import flash
import todo_app.data.trello_items as trello
from todo_app.flask_config import Config
from todo_app.models.ApiException import ApiException
from todo_app.view_models.item_view_model import ItemViewModel

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = []
    try:
        items = trello.get_items()
    except ApiException as err:
        flash(err.message, "error")

    sorted_items = sorted(items, key=lambda item: item.status, reverse=True)
    item_view_model = ItemViewModel(sorted_items)
    return render_template("index.html", view_model=item_view_model)

@app.route('/item', methods=['POST'])
def add_item():
    title = request.form.get("item_title")
    try:
        trello.add_item(title)
        flash("Added new to-do item", "success")
    except ApiException as err:
        flash(err.message, "error")

    return redirect("/")
    return render_template("index.html", view_model=item_view_model)

@app.route('/items/<id>/start', methods=['POST'])
def start_item(id):
    try:
        trello.start_item(id)
        flash("STarted to-do item", "success")
    except ApiException as err:
        flash(err.message, "error")

    return redirect('/')

@app.route('/items/<id>/complete', methods=['POST'])
def complete_item(id):
    try:
        trello.complete_item(id)
        flash("Completed to-do item", "success")
    except ApiException as err:
        flash(err.message, "error")

    return redirect('/')

@app.route('/items/delete/<id>', methods=['POST'])
def delete_item(id):
    try:
        trello.delete_item(id)
        flash("Deleted to-do item", "success")
    except ApiException as err:
        flash(err.message, "error")

    return redirect('/')

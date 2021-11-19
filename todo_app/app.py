from flask import Flask, redirect, render_template, request
import  todo_app.data.session_items as session
import todo_app.data.trello_items as trello
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = trello.get_items()
    sorted_items = sorted(items, key=lambda item: item.status, reverse=True)
    return render_template("index.html", items=sorted_items)

@app.route('/item', methods=['POST'])
def add_item():
    title = request.form.get("item_title")
    trello.add_item(title)
    return redirect("/")

@app.route('/items/<id>', methods=['POST'])
def update_item(id):
    trello.complete_item(id)
    return redirect('/')

@app.route('/items/delete/<id>', methods=['POST'])
def delete_item(id):
    session.remove_item(id)
    return redirect('/')

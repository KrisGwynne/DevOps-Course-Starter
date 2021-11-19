from flask import Flask, redirect, render_template, request
import  todo_app.data.session_items as session
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = session.get_items()
    sorted_items = sorted(items, key=lambda item: item['status'], reverse=True)
    return render_template("index.html", items=sorted_items)

@app.route('/item', methods=['POST'])
def add_item():
    title = request.form.get("item_title")
    session.add_item(title)
    return redirect("/")

@app.route('/items/<id>', methods=['POST'])
def update_item(id):
    item = session.get_item(id)
    item['status'] = 'Completed'
    session.save_item(item)
    return redirect('/')

@app.route('/items/delete/<id>', methods=['POST'])
def delete_item(id):
    session.remove_item(id)
    return redirect('/')

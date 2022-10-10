from functools import wraps
from flask import Flask, redirect, render_template, request, current_app
from flask.helpers import flash
from todo_app.data.item_service import ItemService
from todo_app.flask_config import Config
from todo_app.models.ApiException import ApiException
from todo_app.models.User import AnonymousUser, User
from todo_app.view_models.item_view_model import ItemViewModel
from flask_login import LoginManager, login_required, login_user, current_user
import requests
import os


def check_authorisation(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        login_disabled = current_app.config["LOGIN_DISABLED"]
        if((not login_disabled) and current_user.get_role() != 'writer'):
            flash("You are not authorised to do this action", "error")
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    itemService = ItemService()
    login_manager = LoginManager()
    login_manager.anonymous_user = AnonymousUser

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(f'https://github.com/login/oauth/authorize?client_id={os.getenv("GITHUB_CLIENT_ID")}')

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)

    @app.route('/')
    @login_required
    def index():
        items = []
        try:
            items = itemService.get_items()
        except ApiException as err:
            flash(err.message, "error")

        sorted_items = sorted(items, key=lambda item: item.status, reverse=True)
        item_view_model = ItemViewModel(sorted_items, current_user.get_role())
        return render_template("index.html", view_model=item_view_model)

    @app.route('/item', methods=['POST'])
    @login_required
    @check_authorisation
    def add_item():
        title = request.form.get("item_title")
        try:
            itemService.add_item(title)
            flash("Added new to-do item", "success")
        except ApiException as err:
            flash(err.message, "error")

        return redirect("/")

    @app.route('/items/<id>/start', methods=['POST'])
    @login_required
    @check_authorisation
    def start_item(id):
        try:
            itemService.start_item(id)
            flash("Started to-do item", "success")
        except ApiException as err:
            flash(err.message, "error")

        return redirect('/')

    @app.route('/items/<id>/complete', methods=['POST'])
    @login_required
    @check_authorisation
    def complete_item(id):
        try:
            itemService.complete_item(id)
            flash("Completed to-do item", "success")
        except ApiException as err:
            flash(err.message, "error")

        return redirect('/')

    @app.route('/items/delete/<id>', methods=['POST'])
    @login_required
    @check_authorisation
    def delete_item(id):
        try:
            itemService.delete_item(id)
            flash("Deleted to-do item", "success")
        except ApiException as err:
            flash(err.message, "error")

        return redirect('/')

    @app.route('/login/callback')
    def github_callback():
        github_code = request.args.get("code")

        params = { 
            'client_id': os.getenv("GITHUB_CLIENT_ID"),
            'client_secret': os.getenv("GITHUB_CLIENT_SECRET"),
            'code': github_code
            }
        access_token_res = requests.post("https://github.com/login/oauth/access_token", params, headers={ 'Accept': 'application/json'})
        github_access_token = access_token_res.json()['access_token']

        user_res = requests.get("https://api.github.com/user", headers={ 'Authorization': f'Bearer {github_access_token}'})
        user = User(user_res.json()['id'])

        login_user(user)

        return redirect('/')
    
    return app

from flask import Flask
from main.blueprint.auth_blueprint import auth


def create_app(name):
    flask_app = Flask(name)
    flask_app.register_blueprint(auth, url_prefix='/auth')
    return flask_app

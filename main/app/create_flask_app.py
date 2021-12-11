from flask import Flask
from main.blueprint.auth.auth_blueprint import create_blueprint
from dotenv import load_dotenv


def create_app(name):
    load_dotenv()
    flask_app = Flask(name)
    flask_app.register_blueprint(create_blueprint(), url_prefix='/auth')
    return flask_app

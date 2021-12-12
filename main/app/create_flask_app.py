from flask import Flask
from main.blueprint.auth.auth_blueprint import create_blueprint
from dotenv import load_dotenv
import os
from dotenv.main import find_dotenv


def create_app(name):
    load_profile_specific_dotenv()
    flask_app = Flask(name)
    flask_app.register_blueprint(create_blueprint(), url_prefix='/auth')
    return flask_app


def load_profile_specific_dotenv():
    env = None
    if 'ENV' in os.environ:
        env = os.environ['ENV']

    if env == 'PROD':
        dotenv_path = find_dotenv('.env.docker-prod')
    else:
        dotenv_path = find_dotenv('.env')

    load_dotenv(dotenv_path)

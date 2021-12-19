from flask import Flask
from main.blueprint.auth.auth_blueprint import create_blueprint
from dotenv import load_dotenv
import os
from dotenv.main import find_dotenv
import logging.config
import yaml


def create_app(name):
    load_profile_specific_dotenv()
    init_profile_specific_logging()

    logger = logging.getLogger('fileLogger')
    logger.debug('Инициализация auth-app version=' + os.environ['version'])
    logger.debug('Инициализация flask')

    try:
        flask_app = Flask(name)
        flask_app.register_blueprint(create_blueprint(), url_prefix='/auth')

        logger.debug('Запуск приложения')
        return flask_app
    except Exception as e:
        logger.exception('create app')
        raise e


def init_profile_specific_logging():
    with open(os.path.dirname(__file__) + '/../logging.yml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    log_output_path = os.path.dirname(__file__) + '/../..' + os.environ['log_dir']
    config["handlers"]["file"]["filename"] = config["handlers"]["file"]["filename"].format(log_path=log_output_path)
    logging.config.dictConfig(config)


def load_profile_specific_dotenv():
    env = None
    if 'ENV' in os.environ:
        env = os.environ['ENV']

    if env == 'PROD':
        dotenv_path = find_dotenv('.env.docker-prod')
    else:
        dotenv_path = find_dotenv('.env')

    load_dotenv(dotenv_path)

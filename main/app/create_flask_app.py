from flask import Flask

from main.app import const
from main.blueprint.auth.auth_blueprint import create_blueprint
from dotenv import load_dotenv
import os
from dotenv.main import find_dotenv
import logging.config
import yaml


def create_app(name):
    load_profile_specific_dotenv()
    init_profile_specific_logging()

    logger = logging.getLogger(const.FILE_LOGGER_PARAM_CODE)
    logger.debug('Инициализация auth-app version=' + os.environ[const.ENV_VERSION_PARAM_CODE])
    logger.debug('Инициализация flask')
    if const.ENV_PROFILE_CODE in os.environ:
        logger.debug('Используется профиль - \'' + os.environ[const.ENV_PROFILE_CODE] + '\'')
    else:
        os.environ[const.ENV_PROFILE_CODE] = const.DEV_PROFILE_CODE
        logger.debug('Используется профиль -' + os.environ[const.ENV_PROFILE_CODE])

    try:
        flask_app = Flask(name)
        flask_app.register_blueprint(create_blueprint(), url_prefix=const.AUTH_REST_MAIN_AUTH_PREFIX)

        logger.debug('Запуск приложения')
        return flask_app
    except Exception as e:
        logger.exception('create app')
        raise e


def init_profile_specific_logging():
    with open(os.path.dirname(__file__) + '/../logging.yml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    log_output_path = os.path.dirname(__file__) + '/../..' + os.environ[const.ENV_LOG_DIR_PARAM_CODE]
    config["handlers"]["file"]["filename"] = config["handlers"]["file"]["filename"].format(log_path=log_output_path)
    logging.config.dictConfig(config)


def load_profile_specific_dotenv():
    env = None
    if const.ENV_PROFILE_CODE in os.environ:
        env = os.environ[const.ENV_PROFILE_CODE]

    if env == const.PROD_PROFILE_CODE:
        dotenv_path = find_dotenv('.env.docker-prod')
    else:
        dotenv_path = find_dotenv('.env')

    load_dotenv(dotenv_path)

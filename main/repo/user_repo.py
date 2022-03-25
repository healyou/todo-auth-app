from __future__ import annotations

import json
import logging
import os
import threading

import requests

from main.app import const
from main.entity.users_app import UserData


class _UserRepository:
    _lock = threading.Lock()
    users_app_url = None
    logger = None

    @staticmethod
    def get_instance() -> _UserRepository:
        return _UserRepository()

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            with cls._lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = super(_UserRepository, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.users_app_url = os.environ.get(const.ENV_USERS_APP_URL_PARAM_CODE)
        self.logger = logging.getLogger(const.FILE_LOGGER_PARAM_CODE)

    def get_user_public_id(self, username) -> int | None:
        payload_tuples = [(const.USERS_APP_REST_USERNAME_HEADER_CODE, username)]
        r = requests.post(self.users_app_url + const.USERS_APP_REST_GET_USER_ID_URL, data=payload_tuples)

        if r.status_code == 200 and r.text.isnumeric():
            return int(r.text)
        else:
            self.logger.error(r)
            return None

    def get_user_data(self, username) -> UserData | None:
        payload_tuples = [(const.USERS_APP_REST_USERNAME_HEADER_CODE, username)]
        r = requests.post(self.users_app_url + const.USERS_APP_REST_GET_USER_DATA_URL, data=payload_tuples)

        if r.status_code == 200 and r.text:
            obj = json.loads(r.text)
            return UserData(
                obj[const.USERS_APP_JSON_USER_ID_CODE],
                obj[const.USERS_APP_JSON_PRIVILEGES_CODE]
            )
        else:
            self.logger.error(r)
            return None

    def login(self, username, password) -> bool:
        payload_tuples = [(const.USERS_APP_REST_USERNAME_HEADER_CODE, username), (const.USERS_APP_REST_PASSWORD_HEADER_CODE, password)]
        r = requests.post(self.users_app_url.__str__() + const.USERS_APP_REST_LOGIN_URL, data=payload_tuples)

        if r.status_code == 200:
            if r.text == const.USERS_APP_SUCCESS_TEXT:
                return True
            else:
                self.logger.warning(r)
                return False
        else:
            return False

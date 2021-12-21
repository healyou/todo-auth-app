from __future__ import annotations
import requests
import os
import logging
import threading


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
        self.users_app_url = os.environ.get('users_app_url')
        self.logger = logging.getLogger('fileLogger')

    def get_user_public_id(self, username) -> int | None:
        payload_tuples = [('username', username)]
        r = requests.post(self.users_app_url + '/users/getUserId', data=payload_tuples)

        if r.status_code == 200 and r.text.isnumeric():
            return int(r.text)
        else:
            self.logger.warning(r)
            return None

    def login(self, username, password) -> bool:
        payload_tuples = [('username', username), ('password', password)]
        r = requests.post(self.users_app_url.__str__() + '/users/login', data=payload_tuples)

        if r.status_code == 200 and r.text == 'true':
            if r.text == 'true':
                return True
            else:
                self.logger.warning(r)
                return False
        else:
            return False

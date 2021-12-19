from __future__ import annotations
import requests
import os
import logging


# TODO начитка юзеров из другого приложения
class UserRepository:
    users_app_url = None
    logger = None
    #TODO mock in app tests

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


import uuid
from typing import Tuple

import jwt
from datetime import datetime, timedelta
from main.entity.users_app import UserData
import os
import pytz
from main.app import const


class JwtProvider:
    access_token_secret = None
    refresh_token_secret = None
    algorithm = None
    access_token_time_minutes = None
    refresh_token_time_minutes = None

    def __init__(self):
        self.access_token_secret = os.environ.get(const.ENV_ACCESS_TOKEN_SECRET_PARAM_CODE)
        self.refresh_token_secret = os.environ.get(const.ENV_REFRESH_TOKEN_SECRET_PARAM_CODE)
        self.algorithm = os.environ.get(const.ENV_ALGORITHM_PARAM_CODE)
        self.access_token_time_minutes = int(os.environ.get(const.ENV_ACCESS_TOKEN_TIME_PARAM_CODE))
        self.refresh_token_time_minutes = int(os.environ.get(const.ENV_REFRESH_TOKEN_TIME_PARAM_CODE))

    def encode_access_token(self, username, userdata: UserData) -> Tuple[str, datetime]:
        access_token_expired_time = datetime.utcnow() + timedelta(minutes=self.access_token_time_minutes)
        return jwt.encode(
            {
                const.TOKEN_USERNAME_PAYLOAD_PARAM_CODE: username,
                const.TOKEN_USER_ID_PAYLOAD_PARAM_CODE: userdata.userId,
                const.TOKEN_PRIVILEGES_PAYLOAD_PARAM_CODE: userdata.privileges,
                const.TOKEN_EXP_PAYLOAD_PARAM_CODE: access_token_expired_time
            },
            self.access_token_secret,
            algorithm=self.algorithm
        ), pytz.timezone('Europe/Moscow').localize(access_token_expired_time)

    def encode_refresh_token(self, username, userdata: UserData):
        refresh_token_expired_time = datetime.utcnow() + timedelta(minutes=self.refresh_token_time_minutes)
        return jwt.encode(
            {
                const.TOKEN_USERNAME_PAYLOAD_PARAM_CODE: username,
                const.TOKEN_USER_ID_PAYLOAD_PARAM_CODE: userdata.userId,
                const.TOKEN_PRIVILEGES_PAYLOAD_PARAM_CODE: userdata.privileges,
                const.TOKEN_UUID_PAYLOAD_PARAM_CODE: uuid.uuid4().__str__(),  # random uuid
                const.TOKEN_EXP_PAYLOAD_PARAM_CODE: refresh_token_expired_time
            },
            self.refresh_token_secret,
            algorithm=self.algorithm
        )

    def decode_access_token(self, access_token):
        return jwt.decode(
            access_token,
            self.access_token_secret,
            algorithms=[self.algorithm]
        )

    def decode_refresh_token(self, refresh_token):
        return jwt.decode(
            refresh_token,
            self.refresh_token_secret,
            algorithms=[self.algorithm]
        )

    @staticmethod
    def get_username_from_access_or_refresh_token(token_payload) -> str:
        return token_payload[const.TOKEN_USERNAME_PAYLOAD_PARAM_CODE]

    @staticmethod
    def get_userdata_from_access_or_refresh_token(token_payload) -> UserData:
        return UserData(
            token_payload[const.TOKEN_USER_ID_PAYLOAD_PARAM_CODE],
            token_payload[const.TOKEN_PRIVILEGES_PAYLOAD_PARAM_CODE]
        )

    def get_refresh_token_uuid(self, refresh_token) -> str:
        data = self.decode_refresh_token(refresh_token)
        return data[const.TOKEN_UUID_PAYLOAD_PARAM_CODE]

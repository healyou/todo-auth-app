from __future__ import annotations

import logging
import os
import threading
from datetime import timedelta

import redis

from main.app import const
from main.provider.jwt_provider import JwtProvider


class _TokenRepository:
    _lock = threading.Lock()
    redis_db = None
    refresh_expires = None
    jwt_provider = None
    logger = None

    @staticmethod
    def get_instance() -> _TokenRepository:
        return _TokenRepository()

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            with cls._lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = super(_TokenRepository, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.redis_db = redis.StrictRedis(
            host=os.environ.get(const.ENV_REDIS_HOST_PARAM_CODE),
            port=int(os.environ.get(const.ENV_REDIS_PORT_PARAM_CODE)),
            db=int(os.environ.get(const.ENV_REDIS_DB_NUMBER_PARAM_CODE)),
            password=os.environ.get(const.ENV_REDIS_PASSWORD_PARAM_CODE),
            decode_responses=True
        )
        refresh_token_time_minutes = int(os.environ.get(const.ENV_REFRESH_TOKEN_TIME_PARAM_CODE))
        self.refresh_expires = timedelta(minutes=refresh_token_time_minutes)
        self.jwt_provider = JwtProvider()
        self.logger = logging.getLogger(const.FILE_LOGGER_PARAM_CODE)

    def add_refresh_token(self, refresh_token):
        try:
            uuid = self.jwt_provider.get_refresh_token_uuid(refresh_token)
            self.redis_db.set(uuid, "", ex=self.refresh_expires)
        except Exception:
            self.logger.error('add_refresh_token')

    def has_active_refresh_token(self, refresh_token) -> bool:
        try:
            uuid = self.jwt_provider.get_refresh_token_uuid(refresh_token)
            return self.redis_db.get(uuid) is not None
        except Exception:
            self.logger.exception('has_active_refresh_token')
            return False

    def remove_refresh_token(self, refresh_token):
        try:
            uuid = self.jwt_provider.get_refresh_token_uuid(refresh_token)
            self.redis_db.delete(uuid)
        except Exception:
            self.logger.exception('remove_refresh_token')

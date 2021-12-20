from __future__ import annotations
import redis
import os
from datetime import timedelta
from main.provider.jwt_provider import JwtProvider
import logging
import threading


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
            host=os.environ.get('redis_host'),
            port=int(os.environ.get('redis_port')),
            db=int(os.environ.get('redis_db_number')),
            password=os.environ.get('redis_password'),
            decode_responses=True
        )
        refresh_token_time_minutes = int(os.environ.get('refresh_token_time_minutes'))
        self.refresh_expires = timedelta(minutes=refresh_token_time_minutes)
        self.jwt_provider = JwtProvider()
        self.logger = logging.getLogger('fileLogger')

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

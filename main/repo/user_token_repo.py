import redis
import os
from datetime import timedelta
from main.provider.jwt_provider import JwtProvider
import logging


class UserToken:
    user_id = None
    access_token = None
    refresh_token = None

    def __init__(self, user_id, access_token, refresh_token):
        self.user_id = user_id
        self.access_token = access_token
        self.refresh_token = refresh_token


class TokenRepository:
    tokens = {}
    redis_db = None
    refresh_expires = None
    jwt_provider = None
    logger = None

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

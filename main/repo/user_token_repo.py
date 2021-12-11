import redis
import os
from datetime import timedelta
from main.provider.jwt_provider import JwtProvider


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

    def add_refresh_token(self, refresh_token):
        uuid = self.jwt_provider.get_refresh_token_uuid(refresh_token)
        self.redis_db.set(uuid, "", ex=self.refresh_expires)

    def has_active_refresh_token(self, refresh_token) -> bool:
        uuid = self.jwt_provider.get_refresh_token_uuid(refresh_token)
        return self.redis_db.get(uuid) is not None

    def remove_refresh_token(self, refresh_token):
        uuid = self.jwt_provider.get_refresh_token_uuid(refresh_token)
        self.redis_db.delete(uuid)

    # TODO redis для хранение заблоченных рефреш токенов
    # только операции logout and refresh
    # TODO https://flask-jwt-extended.readthedocs.io/en/stable/blocklist_and_token_revoking/ flask jwt

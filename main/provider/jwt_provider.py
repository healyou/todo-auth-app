import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


class JwtProvider:
    # TODO грузить ключи безопасно
    access_token_secret = None
    refresh_token_secret = None
    algorithm = None
    access_token_time_minutes = None
    refresh_token_time_minutes = None

    def __init__(self):
        # TODO env для dev-qa и других стендов?
        load_dotenv()
        self.access_token_secret = os.environ.get('access_token_secret')
        self.refresh_token_secret = os.environ.get('refresh_token_secret')
        self.algorithm = os.environ.get('algorithm')
        self.access_token_time_minutes = int(os.environ.get('access_token_time_minutes'))
        self.refresh_token_time_minutes = int(os.environ.get('refresh_token_time_minutes'))

    def encode_access_token(self, username):
        access_token_expired_time = datetime.utcnow() + timedelta(minutes=self.access_token_time_minutes)
        return jwt.encode(
            {
                'username': username,
                'exp': access_token_expired_time
            },
            self.access_token_secret,
            algorithm=self.algorithm
        )

    def encode_refresh_token(self, username):
        refresh_token_expired_time = datetime.utcnow() + timedelta(minutes=self.refresh_token_time_minutes)
        return jwt.encode(
            {
                'username': username,
                'exp': refresh_token_expired_time
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

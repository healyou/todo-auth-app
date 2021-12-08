class UserToken:
    user_id = None
    access_token = None
    refresh_token = None

    def __init__(self, user_id, access_token, refresh_token):
        self.user_id = user_id
        self.access_token = access_token
        self.refresh_token = refresh_token


# TODO сохранять в REDIS?
class TokenRepository:
    tokens = {}

    def __init__(self):
        pass

    def save_user_tokens(self, user_token):
        self.tokens[user_token.user_id] = user_token

    def has_access_token(self, username, access_token):
        return username in self.tokens and self.tokens[username].access_token == access_token

    def has_refresh_token(self, username, refresh_token):
        return username in self.tokens and self.tokens[username].refresh_token == refresh_token

    def remove_user_token(self, user_id):
        if user_id in self.tokens:
            del self.tokens[user_id]
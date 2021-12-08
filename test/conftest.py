from main.app.create_flask_app import create_app
import pytest


@pytest.fixture
def app():
    app = create_app('test_app')
    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


class AuthActions:
    login_url = '/auth/login'
    logout_url = '/auth/logout'
    refresh_token_url = '/auth/refreshToken'
    validate_token_url = '/auth/validateToken'

    def __init__(self, client):
        self._client = client

    def login(self, username='1', password='password'):
        return self._client.post(
            self.login_url, data={'username': username, 'password': password}
        )

    def logout(self, access_token):
        headers = {'X-Access-Token': access_token}
        return self._client.post(self.logout_url, headers=headers)


@pytest.fixture
def auth_actions(client):
    return AuthActions(client)

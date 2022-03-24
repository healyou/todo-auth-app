import logging
import os

import pytest

from main.app.create_flask_app import create_app
from main.provider.jwt_provider import JwtProvider
from main.entity.users_app import UserData


ERROR_LOGIN_NAME = 'error'


@pytest.fixture
def app(mocker):
    mock_repo(mocker)
    app = create_app('test_app')
    return app


def mock_repo(session_mocker):
    if 'ENV' in os.environ and os.environ['ENV'] == 'UNIT_TEST':
        mock_token_repo = mock_user_token_repo(session_mocker)
        mock_repo_user = mock_user_repo(session_mocker)
        session_mocker.patch(
            'main.repo.repo_creator.get_user_token_repo',
            return_value=mock_token_repo
        )
        session_mocker.patch(
            'main.repo.repo_creator.get_user_repo',
            return_value=mock_repo_user
        )
    elif 'ENV' in os.environ and os.environ['ENV'] == 'INTEGRATION_TEST':
        mock_repo_user = mock_user_repo(session_mocker)
        session_mocker.patch(
            'main.repo.repo_creator.get_user_repo',
            return_value=mock_repo_user
        )
    else:
        # все сервисы должны быть запущены (redis + users-app)
        pass


def mock_user_repo(session_mocker):
    mock = session_mocker.MagicMock()

    def mock_login(*args, **kwargs):
        # со второго вызова нельзя использовать токен
        if args[0] == ERROR_LOGIN_NAME:
            return False
        else:
            return True

    user_id = 1
    privileges = ["test"]
    user_data = UserData(user_id, privileges)
    mock.configure_mock(
        **{
            "get_instance.return_value": mock,
            "get_user_public_id.return_value": user_id,
            "get_user_data.return_value": user_data,
            "login.side_effect": mock_login
        }
    )
    return mock


def mock_user_token_repo(session_mocker):
    mock = session_mocker.MagicMock()

    def mock_has_active_refresh_token(*args, **kwargs):
        # со второго вызова нельзя использовать токен
        if mock.has_active_refresh_token.call_count >= 2:
            return False
        else:
            return True

    mock.configure_mock(
        **{
            "get_instance.return_value": mock,
            "has_active_refresh_token.side_effect": mock_has_active_refresh_token
        }
    )
    return mock


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


class AuthActions:
    login_url = '/auth/login'
    logout_url = '/auth/logout'
    refresh_token_url = '/auth/refreshToken'
    validate_token_url = '/auth/validateToken'
    error_login = ERROR_LOGIN_NAME

    def __init__(self, client):
        self._client = client

    def login(self, username='admin', password='admin'):
        return self._client.post(
            self.login_url, data={'username': username, 'password': password}
        )

    def refresh_token(self, refresh_token):
        headers = {'X-Refresh-Token': refresh_token}
        return self._client.post(self.refresh_token_url, headers=headers)

    def logout(self, access_token, refresh_token):
        headers = {
            'X-Access-Token': access_token,
            'X-Refresh-Token': refresh_token
        }
        return self._client.post(self.logout_url, headers=headers)


@pytest.fixture
def auth_actions(client):
    return AuthActions(client)


@pytest.fixture
def jwt_provider():
    return JwtProvider()

import os
import uuid

import pytest

from main.app import const
from main.app.create_flask_app import create_app
from main.entity.users_app import UserData
from main.provider.jwt_provider import JwtProvider

ERROR_LOGIN_NAME = uuid.uuid4().__str__()


@pytest.fixture
def app(mocker):
    mock_repo(mocker)
    app = create_app('test_app')
    return app


def mock_repo(session_mocker):
    if const.ENV_PROFILE_CODE in os.environ and os.environ[const.ENV_PROFILE_CODE] == const.UNIT_TEST_PROFILE_CODE:
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
    elif const.ENV_PROFILE_CODE in os.environ and os.environ[const.ENV_PROFILE_CODE] == const.INTEGRATION_TEST_PROFILE_CODE:
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
    TEST_LOGIN_USERNAME = 'admin'
    TEST_LOGIN_PASSWORD = 'admin'

    login_url = const.AUTH_REST_MAIN_AUTH_PREFIX + const.AUTH_REST_LOGIN_PREFIX
    logout_url = const.AUTH_REST_MAIN_AUTH_PREFIX + const.AUTH_REST_LOGOUT_PREFIX
    refresh_token_url = const.AUTH_REST_MAIN_AUTH_PREFIX + const.AUTH_REST_REFRESH_TOKEN_PREFIX
    validate_token_url = const.AUTH_REST_MAIN_AUTH_PREFIX + const.AUTH_REST_VALIDATE_TOKEN_PREFIX
    error_login = ERROR_LOGIN_NAME

    def __init__(self, client):
        self._client = client

    def login(self, username=TEST_LOGIN_USERNAME, password=TEST_LOGIN_PASSWORD):
        return self._client.post(
            self.login_url, data={
                const.USERS_APP_REST_USERNAME_HEADER_CODE: username, const.USERS_APP_REST_PASSWORD_HEADER_CODE: password
            }
        )

    def refresh_token(self, refresh_token):
        headers = {const.JSON_IN_REFRESH_TOKEN_CODE: refresh_token}
        return self._client.post(self.refresh_token_url, headers=headers)

    def logout(self, access_token, refresh_token):
        headers = {
            const.JSON_IN_ACCESS_TOKEN_CODE: access_token,
            const.JSON_IN_REFRESH_TOKEN_CODE: refresh_token
        }
        return self._client.post(self.logout_url, headers=headers)


@pytest.fixture
def auth_actions(client):
    return AuthActions(client)


@pytest.fixture
def jwt_provider():
    return JwtProvider()

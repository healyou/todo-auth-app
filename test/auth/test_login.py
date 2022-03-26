import jwt

from main.app import const


def test_login_successful(client, auth_actions):
    response = auth_actions.login()
    assert response.status_code == 201
    assert response.json[const.JSON_OUT_ACCESS_TOKEN_CODE]
    assert response.json[const.JSON_OUT_REFRESH_TOKEN_CODE]


def test_login_incorrect_data(client, auth_actions):
    response = auth_actions.login(auth_actions.error_login, auth_actions.error_login)
    assert response.status_code == 401


def test_login_no_data(client, auth_actions):
    response = client.post(auth_actions.login_url)
    assert response.status_code == 401


def test_login_success_tokens_struct(client, auth_actions, jwt_provider):
    response = auth_actions.login()

    access_token = response.json[const.JSON_OUT_ACCESS_TOKEN_CODE]
    access_token_data = jwt.decode(
        access_token, options={"verify_signature": False}, algorithms=[jwt_provider.algorithm]
    )

    assert access_token_data[const.TOKEN_USERNAME_PAYLOAD_PARAM_CODE] == auth_actions.TEST_LOGIN_USERNAME
    assert access_token_data[const.TOKEN_USER_ID_PAYLOAD_PARAM_CODE] is not None
    assert access_token_data[const.TOKEN_PRIVILEGES_PAYLOAD_PARAM_CODE] is not None
    assert access_token_data[const.TOKEN_EXP_PAYLOAD_PARAM_CODE] is not None

    refresh_token = response.json[const.JSON_OUT_REFRESH_TOKEN_CODE]
    refresh_token_data = jwt.decode(
        refresh_token, options={"verify_signature": False}, algorithms=[jwt_provider.algorithm]
    )

    assert refresh_token_data[const.TOKEN_USERNAME_PAYLOAD_PARAM_CODE] == auth_actions.TEST_LOGIN_USERNAME
    assert refresh_token_data[const.TOKEN_USER_ID_PAYLOAD_PARAM_CODE] is not None
    assert refresh_token_data[const.TOKEN_PRIVILEGES_PAYLOAD_PARAM_CODE] is not None
    assert len(refresh_token_data[const.TOKEN_UUID_PAYLOAD_PARAM_CODE]) > 0
    assert refresh_token_data[const.TOKEN_EXP_PAYLOAD_PARAM_CODE] is not None

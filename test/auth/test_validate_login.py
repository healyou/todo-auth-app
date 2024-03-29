from main.app import const


def test_validate_login_on_access_token(client, auth_actions):
    response = auth_actions.login()
    access_token = response.json[const.JSON_OUT_ACCESS_TOKEN_CODE]

    headers = {const.JSON_IN_ACCESS_TOKEN_CODE: access_token}
    response = client.post(auth_actions.validate_token_url, headers=headers)
    assert response.status_code == 200


def test_validate_login_on_refresh_token(client, auth_actions):
    response = auth_actions.login()
    refresh_token = response.json[const.JSON_OUT_REFRESH_TOKEN_CODE]

    headers = {const.JSON_IN_ACCESS_TOKEN_CODE: refresh_token}
    response = client.post(auth_actions.validate_token_url, headers=headers)
    assert response.status_code == 401


def test_validate_login_no_header(client, auth_actions):
    auth_actions.login()
    response = client.post(auth_actions.validate_token_url)
    assert response.status_code == 401

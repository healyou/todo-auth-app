from main.app import const


def test_logout_successful(client, auth_actions):
    response = auth_actions.login()
    access_token = response.json[const.JSON_OUT_ACCESS_TOKEN_CODE]
    refresh_token = response.json[const.JSON_OUT_REFRESH_TOKEN_CODE]
    response = auth_actions.logout(access_token, refresh_token)
    assert response.status_code == 200


def test_double_logout(client, auth_actions):
    response = auth_actions.login()
    access_token = response.json[const.JSON_OUT_ACCESS_TOKEN_CODE]
    refresh_token = response.json[const.JSON_OUT_REFRESH_TOKEN_CODE]
    auth_actions.logout(access_token, refresh_token)
    response = auth_actions.logout(access_token, refresh_token)
    assert response.status_code == 401


def test_logout_no_login(client, auth_actions):
    response = client.post(auth_actions.logout_url)
    assert response.status_code == 401


def test_logout_by_refresh_token(client, auth_actions):
    response = auth_actions.login()
    access_token = response.json[const.JSON_OUT_ACCESS_TOKEN_CODE]
    refresh_token = response.json[const.JSON_OUT_REFRESH_TOKEN_CODE]
    response = auth_actions.logout(refresh_token, access_token)
    assert response.status_code == 401


def test_logout_by_no_headers(client, auth_actions):
    auth_actions.login()
    response = client.post(auth_actions.logout_url)
    assert response.status_code == 401

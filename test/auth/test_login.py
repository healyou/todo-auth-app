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

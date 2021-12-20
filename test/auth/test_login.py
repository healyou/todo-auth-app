def test_login_successful(client, auth_actions):
    response = auth_actions.login()
    assert response.status_code == 201
    assert response.json['access_token']
    assert response.json['refresh_token']


def test_login_incorrect_data(client, auth_actions):
    response = auth_actions.login(auth_actions.error_login, auth_actions.error_login)
    assert response.status_code == 401


def test_login_no_data(client, auth_actions):
    response = client.post(auth_actions.login_url)
    assert response.status_code == 401

def test_logout_successful(client, auth_actions):
    response = auth_actions.login()
    access_token = response.json['access_token']
    response = auth_actions.logout(access_token)
    assert response.status_code == 200


def test_logout_no_login(client, auth_actions):
    response = client.post(auth_actions.logout_url)
    assert response.status_code == 401


def test_logout_by_refresh_token(client, auth_actions):
    response = auth_actions.login()
    refresh_token = response.json['refresh_token']
    response = auth_actions.logout(refresh_token)
    assert response.status_code == 401


def test_logout_by_no_headers(client, auth_actions):
    auth_actions.login()
    response = client.post(auth_actions.logout_url)
    assert response.status_code == 401

def test_get_refresh_token_successful(client, auth_actions):
    response = auth_actions.login()
    refresh_token = response.json['refresh_token']

    headers = {'X-Refresh-Token': refresh_token}
    response = client.post(auth_actions.refresh_token_url, headers=headers)
    assert response.status_code == 201
    assert response.json['access_token']
    assert response.json['refresh_token']


def test_get_refresh_token_by_access_token(client, auth_actions):
    response = auth_actions.login()
    access_token = response.json['access_token']

    headers = {'X-Refresh-Token': access_token}
    response = client.post(auth_actions.refresh_token_url, headers=headers)
    assert response.status_code == 401


def test_get_refresh_token_no_header(client, auth_actions):
    auth_actions.login()
    response = client.post(auth_actions.refresh_token_url)
    assert response.status_code == 401


def test_get_refresh_token_double(client, auth_actions):
    response = auth_actions.login()
    refresh_token = response.json['refresh_token']

    auth_actions.refresh_token(refresh_token)
    response = auth_actions.refresh_token(refresh_token)
    assert response.status_code == 401

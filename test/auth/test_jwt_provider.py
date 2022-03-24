from main.entity.users_app import UserData
import jwt


def test_encode_access_token_payload_data(client, jwt_provider):
    username = "test"
    privileges = ["test"]
    userid = 1
    userdata = UserData(userid, privileges)

    access_token, expire_datetime = jwt_provider.encode_access_token(username, userdata)
    token_data = jwt.decode(access_token, options={"verify_signature": False}, algorithms=[jwt_provider.algorithm])

    assert token_data['username'] == username
    assert token_data['user_id'] == userid
    assert token_data['privileges'] == privileges


def test_encode_refresh_token_payload_data(client, jwt_provider):
    username = "test"
    privileges = ["test"]
    userid = 1
    userdata = UserData(userid, privileges)

    refresh_token = jwt_provider.encode_refresh_token(username, userdata)
    token_data = jwt.decode(refresh_token, options={"verify_signature": False}, algorithms=[jwt_provider.algorithm])

    assert token_data['username'] == username
    assert token_data['user_id'] == userid
    assert token_data['privileges'] == privileges
    assert token_data['uuid']

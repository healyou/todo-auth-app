from main.app import const
from main.entity.users_app import UserData
import jwt


def test_encode_access_token_payload_data(client, jwt_provider):
    username = "test"
    privileges = ["test"]
    userid = 1
    userdata = UserData(userid, privileges)

    access_token, expire_datetime = jwt_provider.encode_access_token(username, userdata)
    token_data = jwt.decode(access_token, options={"verify_signature": False}, algorithms=[jwt_provider.algorithm])

    assert token_data[const.TOKEN_USERNAME_PAYLOAD_PARAM_CODE] == username
    assert token_data[const.TOKEN_USER_ID_PAYLOAD_PARAM_CODE] == userid
    assert token_data[const.TOKEN_PRIVILEGES_PAYLOAD_PARAM_CODE] == privileges


def test_encode_refresh_token_payload_data(client, jwt_provider):
    username = "test"
    privileges = ["test"]
    userid = 1
    userdata = UserData(userid, privileges)

    refresh_token = jwt_provider.encode_refresh_token(username, userdata)
    token_data = jwt.decode(refresh_token, options={"verify_signature": False}, algorithms=[jwt_provider.algorithm])

    assert token_data[const.TOKEN_USERNAME_PAYLOAD_PARAM_CODE] == username
    assert token_data[const.TOKEN_USER_ID_PAYLOAD_PARAM_CODE] == userid
    assert token_data[const.TOKEN_PRIVILEGES_PAYLOAD_PARAM_CODE] == privileges
    assert token_data[const.TOKEN_UUID_PAYLOAD_PARAM_CODE]

from flask import Blueprint, request, jsonify, make_response
from main.repo.user_token_repo import TokenRepository, UserToken
from main.provider.jwt_provider import JwtProvider
from main.repo.user_repo import UserRepository
from main.provider.hash_provider import HashProvider
import jwt


auth = Blueprint('auth', __name__)

token_repository = TokenRepository()
jwt_provider = JwtProvider()
user_repository = UserRepository()
hash_provider = HashProvider()


@auth.route('/validateToken', methods=['GET', 'POST'])
def validate_token():
    token = None
    # jwt is passed in the request header
    if 'X-Access-Token' in request.headers:
        token = request.headers['x-access-token']
    # return 401 if token is not passed
    if not token:
        return jsonify({'message': 'Token is missing !!'}), 401

    try:
        # decoding the payload to fetch the stored details
        data = jwt_provider.decode_access_token(token)

        if not token_repository.has_access_token(data['username'], token):
            return jsonify({'message': 'Token is missing !!'}), 401

        return make_response(
            jsonify({'message': 'Token is valid'}),
            200
        )
    except jwt.ExpiredSignatureError:
        return jsonify({
            'message': 'Token is expired !!!'
        }), 401
    except jwt.InvalidTokenError as e:
        return jsonify({
            'message': 'Token is invalid !!!'
        }), 401
    except:
        return jsonify({
            'message': 'Validation Token Exception'
        }), 401


@auth.route('/refreshToken', methods=['POST'])
def refresh_token():
    user_refresh_token = None
    # jwt is passed in the request header
    if 'X-Refresh-Token' in request.headers:
        user_refresh_token = request.headers['x-refresh-token']

    # return 401 if token is not passed
    if not user_refresh_token:
        return jsonify({'message': 'Refresh Token is missing !!'}), 401

    try:
        # decoding the payload to fetch the stored details
        data = jwt_provider.decode_refresh_token(user_refresh_token)

        if not token_repository.has_refresh_token(data['username'], user_refresh_token):
            return jsonify({'message': 'Refresh Token is missing !!'}), 401

        # generates the JWT Token
        new_access_token = jwt_provider.encode_access_token(data['username'])
        # ограниченное время действия, но достаточно большое
        new_user_refresh_token = jwt_provider.encode_refresh_token(data['username'])

        user_token = UserToken(
            data['username'],
            new_access_token,
            new_user_refresh_token
        )
        token_repository.save_user_tokens(user_token)

        return make_response(
            jsonify({
                'access_token': new_access_token,
                # 'access_token_expired_time': access_token_expired_time,
                'refresh_token': new_user_refresh_token
            }),
            201
        )
    except jwt.ExpiredSignatureError:
        return jsonify({
            'message': 'Token is expired !!!'
        }), 401
    except jwt.InvalidTokenError:
        return jsonify({
            'message': 'Token is invalid !!!'
        }), 401
    except Exception as e:
        return jsonify({
            'message': 'Validation Token Exception'
        }), 401


@auth.route('/logout', methods=['POST'])
def logout():
    token = None
    # jwt is passed in the request header
    if 'X-Access-Token' in request.headers:
        token = request.headers['x-access-token']
    # return 401 if token is not passed
    if not token:
        return jsonify({'message': 'Token is missing !!'}), 401

    try:
        data = jwt_provider.decode_access_token(token)
        if not token_repository.has_access_token(data['username'], token):
            return jsonify({
                'message': 'Token is invalid !!!'
            }), 401

        token_repository.remove_user_token(data['username'])

        return make_response(
            jsonify({
                'message': 'successful logout'
            }),
            200
        )
    except jwt.ExpiredSignatureError as e:
        return jsonify({
            'message': 'Token is expired !!!'
        }), 401
    except jwt.InvalidTokenError:
        return jsonify({
            'message': 'Token is invalid !!!'
        }), 401
    except:
        return jsonify({
            'message': 'Validation Token Exception'
        }), 401


@auth.route('/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.form

    if not auth or not auth.get('username') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = user_repository.get_by_username(auth.get('username'))

    if not user or user is None:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    # psw_hash = hash_provider.hash_psw(user.psw_hash)
    if hash_provider.check_psw(auth.get('password'), user.psw_hash):
        # generates the JWT Token
        access_token = jwt_provider.encode_access_token(user.public_id)
        # ограниченное время действия, но достаточно большое
        refresh_token = jwt_provider.encode_refresh_token(user.public_id)

        user_token = UserToken(user.public_id, access_token, refresh_token)
        token_repository.save_user_tokens(user_token)

        return make_response(
            jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token
            }),
            201
        )
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )

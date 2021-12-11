from __future__ import annotations

import datetime

from flask import request, jsonify, make_response


def unsupported_exception_500():
    return jsonify({'message': 'Unsupported exception'})


def token_missing_json_401():
    return jsonify({'message': 'Token is missing !!'}), 401


def token_valid_200():
    return make_response(
        jsonify({'message': 'Token is valid'}),
        200
    )


def token_expired_401():
    return jsonify({
        'message': 'Token is expired'
    }), 401


def token_invalid_401():
    return jsonify({
        'message': 'Token is invalid'
    }), 401


def validation_token_exception_401():
    return jsonify({
        'message': 'Validation Token Exception'
    }), 401


def refresh_token_missing_401():
    return jsonify({'message': 'Refresh Token is missing'}), 401


def refresh_token_blocked_401():
    return jsonify({'message': 'Refresh Token is blocked !!'}), 401


def token_info_201(access_token, access_token_expired_time, refresh_token):
    return make_response(
        jsonify({
            'access_token': access_token,
            'access_token_expired_time_utc': access_token_expired_time.strftime("%m.%d.%Y %H:%M:%S %z"),
            'refresh_token': refresh_token
        }),
        201
    )


def no_auth_info_401():
    return make_response(
        'Could not verify',
        401,
        {'WWW-Authenticate': 'Basic realm ="Login required"'}
    )


def login_success_200():
    return make_response(
        jsonify({
            'message': 'successful logout'
        }),
        200
    )


def get_username_from_form():
    return request.form.get('username')


def get_password_from_form():
    return request.form.get('password')


def not_valid_login_401():
    return make_response(
        'Could not verify',
        401,
        {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
    )


def get_access_token_from_header() -> str | None:
    if 'X-Access-Token' in request.headers:
        return request.headers['x-access-token']
    else:
        return None


def get_refresh_token_from_header() -> str | None:
    if 'X-Refresh-Token' in request.headers:
        return request.headers['x-refresh-token']
    else:
        return None

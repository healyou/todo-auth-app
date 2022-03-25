from __future__ import annotations

from flask import request, jsonify, make_response

from main.app import const


def unsupported_exception_500():
    return jsonify({const.JSON_OUT_MESSAGE_CODE: 'Unsupported exception'}), 500


def token_missing_json_401():
    return jsonify({const.JSON_OUT_MESSAGE_CODE: 'Token is missing !!'}), 401


def token_valid_200():
    return make_response(
        jsonify({const.JSON_OUT_MESSAGE_CODE: 'Token is valid'}),
        200
    )


def token_expired_401():
    return jsonify({
        const.JSON_OUT_MESSAGE_CODE: 'Token is expired'
    }), 401


def token_invalid_401():
    return jsonify({
        const.JSON_OUT_MESSAGE_CODE: 'Token is invalid'
    }), 401


def validation_token_exception_401():
    return jsonify({
        const.JSON_OUT_MESSAGE_CODE: 'Validation Token Exception'
    }), 401


def refresh_token_missing_401():
    return jsonify({const.JSON_OUT_MESSAGE_CODE: 'Refresh Token is missing'}), 401


def refresh_token_blocked_401():
    return jsonify({const.JSON_OUT_MESSAGE_CODE: 'Refresh Token is blocked !!'}), 401


def token_info_201(access_token, access_token_expired_time, refresh_token):
    return make_response(
        jsonify({
            const.JSON_OUT_ACCESS_TOKEN_CODE: access_token,
            const.JSON_OUT_ACCESS_TOKEN_EXPIRED_TIME_UTC_CODE: access_token_expired_time.strftime("%m.%d.%Y %H:%M:%S %z"),
            const.JSON_OUT_REFRESH_TOKEN_CODE: refresh_token
        }),
        201
    )


def no_auth_info_401():
    return make_response(
        'Could not verify',
        401,
        {const.JSON_OUT_AUTH_INFO_CODE: 'Basic realm ="Login required"'}
    )


def login_success_200():
    return make_response(
        jsonify({
            const.JSON_OUT_MESSAGE_CODE: 'successful logout'
        }),
        200
    )


def get_username_from_form():
    return request.form.get(const.JSON_IN_USERNAME_CODE)


def get_password_from_form():
    return request.form.get(const.JSON_IN_PASSWORD_CODE)


def not_valid_login_401():
    return make_response(
        'Could not verify',
        401,
        {const.JSON_OUT_AUTH_INFO_CODE: 'Basic realm ="User does not exist !!"'}
    )


def get_access_token_from_header() -> str | None:
    if const.JSON_IN_ACCESS_TOKEN_CODE in request.headers:
        return request.headers[const.JSON_IN_ACCESS_TOKEN_CODE]
    else:
        return None


def get_refresh_token_from_header() -> str | None:
    if const.JSON_IN_REFRESH_TOKEN_CODE in request.headers:
        return request.headers[const.JSON_IN_REFRESH_TOKEN_CODE]
    else:
        return None

from __future__ import annotations

import logging

import jwt
from flask import Blueprint

import main.repo.repo_creator as repo_creator
from main.blueprint.auth.request_support import *
from main.entity.users_app import UserData
from main.provider.jwt_provider import JwtProvider


def create_blueprint() -> Blueprint:
    auth_bp = Blueprint('auth', __name__)

    # from main.repo.repo_creator import get_user_repo, get_user_token_repo
    token_repository = repo_creator.get_user_token_repo()
    user_repository = repo_creator.get_user_repo()
    jwt_provider = JwtProvider()
    logger = logging.getLogger(const.FILE_LOGGER_PARAM_CODE)

    @auth_bp.route(const.AUTH_REST_VALIDATE_TOKEN_PREFIX, methods=['GET', 'POST'])
    def validate_token():
        try:
            token = get_access_token_from_header()
            if not token:
                logger.debug('missing token on validateToken')
                return token_missing_json_401()

            try:
                jwt_provider.decode_access_token(token)
                return token_valid_200()
            except jwt.ExpiredSignatureError as e:
                logger.warning('validateToken' + e.__str__())
                return token_expired_401()
            except jwt.InvalidTokenError as e:
                logger.warning('validateToken' + e.__str__())
                return token_invalid_401()
            except Exception:
                logger.exception('validateToken')
                return validation_token_exception_401()
        except Exception:
            logger.exception('validateToken')
            return unsupported_exception_500()

    @auth_bp.route(const.AUTH_REST_REFRESH_TOKEN_PREFIX, methods=['POST'])
    def refresh_token():
        try:
            user_refresh_token = get_refresh_token_from_header()
            if not user_refresh_token:
                logger.debug('missing token on refreshToken')
                return refresh_token_missing_401()

            try:
                data = jwt_provider.decode_refresh_token(user_refresh_token)
                username = jwt_provider.get_username_from_access_or_refresh_token(data)
                userdata = jwt_provider.get_userdata_from_access_or_refresh_token(data)

                if not token_repository.has_active_refresh_token(user_refresh_token):
                    logger.debug('refresh token blocked on refreshToken')
                    return refresh_token_blocked_401()

                new_access_token, expire_datetime = jwt_provider.encode_access_token(username, userdata)
                new_user_refresh_token = jwt_provider.encode_refresh_token(username, userdata)

                token_repository.remove_refresh_token(user_refresh_token)
                token_repository.add_refresh_token(new_user_refresh_token)

                return token_info_201(new_access_token, expire_datetime, new_user_refresh_token)
            except jwt.ExpiredSignatureError as e:
                logger.warning('refreshToken' + e.__str__())
                return token_expired_401()
            except jwt.InvalidTokenError as e:
                logger.warning('refreshToken' + e.__str__())
                return token_invalid_401()
            except Exception:
                logger.exception('refreshToken')
                return validation_token_exception_401()
        except Exception:
            logger.exception('refreshToken')
            return unsupported_exception_500()

    @auth_bp.route(const.AUTH_REST_LOGOUT_PREFIX, methods=['POST'])
    def logout():
        try:
            access_token = get_access_token_from_header()
            refresh_token = get_refresh_token_from_header()

            if not access_token or not refresh_token:
                logger.debug('missing token on logout')
                return token_missing_json_401()

            try:
                jwt_provider.decode_access_token(access_token)
                if not token_repository.has_active_refresh_token(refresh_token):
                    logger.debug('invalid token on logout')
                    return token_invalid_401()

                token_repository.remove_refresh_token(refresh_token)
                return login_success_200()
            except jwt.ExpiredSignatureError as e:
                logger.warning('logout' + e.__str__())
                return token_expired_401()
            except jwt.InvalidTokenError as e:
                logger.warning('logout' + e.__str__())
                return token_invalid_401()
            except Exception:
                logger.exception('logout')
                return validation_token_exception_401()
        except Exception:
            logger.exception('logout')
            return unsupported_exception_500()

    @auth_bp.route(const.AUTH_REST_LOGIN_PREFIX, methods=['POST'])
    def login():
        try:
            auth = request.form
            username = get_username_from_form()
            password = get_password_from_form()

            if not auth:
                logger.debug('no auth data on login')
                return no_auth_info_401()
            elif not username or not password:
                logger.debug('no user data on login')
                return no_auth_info_401()

            login = user_repository.login(username, password)

            if not login:
                logger.warning('no find user on login')
                return not_valid_login_401()
            else:
                user_data: UserData = user_repository.get_user_data(username)

                if user_data and user_data.userId:
                    user_public_id = user_data.userId
                    access_token, expire_datetime = jwt_provider.encode_access_token(user_public_id, user_data)
                    refresh_token = jwt_provider.encode_refresh_token(user_public_id, user_data)

                    token_repository.add_refresh_token(refresh_token)
                    return token_info_201(access_token, expire_datetime, refresh_token)
                else:
                    logger.warning('not valid token on login')
                    return not_valid_login_401()
        except Exception as e:
            logger.exception('login')
            return unsupported_exception_500()

    return auth_bp

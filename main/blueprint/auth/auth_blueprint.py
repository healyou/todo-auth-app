from __future__ import annotations
from flask import Blueprint
from main.repo.user_token_repo import TokenRepository
from main.provider.jwt_provider import JwtProvider
from main.repo.user_repo import UserRepository
from main.blueprint.auth.request_support import *
import jwt
import logging


def create_blueprint() -> Blueprint:
    auth_bp = Blueprint('auth', __name__)

    token_repository = TokenRepository()
    jwt_provider = JwtProvider()
    user_repository = UserRepository()
    logger = logging.getLogger('fileLogger')

    @auth_bp.route('/validateToken', methods=['GET', 'POST'])
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

    @auth_bp.route('/refreshToken', methods=['POST'])
    def refresh_token():
        try:
            user_refresh_token = get_refresh_token_from_header()
            if not user_refresh_token:
                logger.debug('missing token on refreshToken')
                return refresh_token_missing_401()

            try:
                data = jwt_provider.decode_refresh_token(user_refresh_token)
                username = jwt_provider.get_username_from_access_or_refresh_token(data)

                if not token_repository.has_active_refresh_token(user_refresh_token):
                    logger.debug('refresh token blocked on refreshToken')
                    return refresh_token_blocked_401()

                new_access_token, expire_datetime = jwt_provider.encode_access_token(username)
                new_user_refresh_token = jwt_provider.encode_refresh_token(username)

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

    @auth_bp.route('/logout', methods=['POST'])
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

    @auth_bp.route('/login', methods=['POST'])
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
                user_public_id = user_repository.get_user_public_id(username)

                if user_public_id:
                    access_token, expire_datetime = jwt_provider.encode_access_token(user_public_id)
                    refresh_token = jwt_provider.encode_refresh_token(user_public_id)

                    token_repository.add_refresh_token(refresh_token)
                    return token_info_201(access_token, expire_datetime, refresh_token)
                else:
                    logger.warning('not valid token on login')
                    return not_valid_login_401()
        except Exception as e:
            logger.exception('login')
            return unsupported_exception_500()

    return auth_bp

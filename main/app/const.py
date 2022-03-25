# token const
TOKEN_USERNAME_PAYLOAD_PARAM_CODE = 'username'
TOKEN_USER_ID_PAYLOAD_PARAM_CODE = 'user_id'
TOKEN_PRIVILEGES_PAYLOAD_PARAM_CODE = 'privileges'
TOKEN_EXP_PAYLOAD_PARAM_CODE = 'exp'
TOKEN_UUID_PAYLOAD_PARAM_CODE = 'uuid'

# env const
ENV_ACCESS_TOKEN_SECRET_PARAM_CODE = 'access_token_secret'
ENV_REFRESH_TOKEN_SECRET_PARAM_CODE = 'refresh_token_secret'
ENV_ALGORITHM_PARAM_CODE = 'algorithm'
ENV_ACCESS_TOKEN_TIME_PARAM_CODE = 'access_token_time_minutes'
ENV_REFRESH_TOKEN_TIME_PARAM_CODE = 'refresh_token_time_minutes'
ENV_USERS_APP_URL_PARAM_CODE = 'users_app_url'
ENV_REDIS_HOST_PARAM_CODE = 'redis_host'
ENV_REDIS_PORT_PARAM_CODE = 'redis_port'
ENV_REDIS_DB_NUMBER_PARAM_CODE = 'redis_db_number'
ENV_REDIS_PASSWORD_PARAM_CODE = 'redis_password'
ENV_VERSION_PARAM_CODE = 'version'
ENV_LOG_DIR_PARAM_CODE = 'log_dir'
ENV_PROFILE_CODE = 'ENV'

# profiles
DEV_PROFILE_CODE = 'DEV'
PROD_PROFILE_CODE = 'PROD'
UNIT_TEST_PROFILE_CODE = 'UNIT_TEST'
INTEGRATION_TEST_PROFILE_CODE = 'INTEGRATION_TEST'

# rest json data codes
JSON_OUT_ACCESS_TOKEN_CODE = 'access_token'
JSON_OUT_REFRESH_TOKEN_CODE = 'refresh_token'
JSON_OUT_ACCESS_TOKEN_EXPIRED_TIME_UTC_CODE = 'access_token_expired_time_utc'
JSON_OUT_MESSAGE_CODE = 'message'
JSON_OUT_AUTH_INFO_CODE = 'WWW-Authenticate'
JSON_IN_USERNAME_CODE = 'username'
JSON_IN_PASSWORD_CODE = 'password'
JSON_IN_ACCESS_TOKEN_CODE = 'X-Access-Token'
JSON_IN_REFRESH_TOKEN_CODE = 'X-Refresh-Token'

# auth rest path codes
AUTH_REST_MAIN_AUTH_PREFIX = '/auth'
AUTH_REST_LOGIN_PREFIX = '/login'
AUTH_REST_LOGOUT_PREFIX = '/logout'
AUTH_REST_REFRESH_TOKEN_PREFIX = '/refreshToken'
AUTH_REST_VALIDATE_TOKEN_PREFIX = '/validateToken'

# user-app rest codes
USERS_APP_REST_USERNAME_HEADER_CODE = 'username'
USERS_APP_REST_PASSWORD_HEADER_CODE = 'password'
USERS_APP_REST_GET_USER_ID_URL = '/users/getUserId'
USERS_APP_REST_GET_USER_DATA_URL = '/users/getUserData'
USERS_APP_REST_LOGIN_URL = '/users/login'
USERS_APP_SUCCESS_TEXT = 'true'
USERS_APP_JSON_USER_ID_CODE = 'userId'
USERS_APP_JSON_PRIVILEGES_CODE = 'privilegeCodes'

# other
FILE_LOGGER_PARAM_CODE = 'fileLogger'

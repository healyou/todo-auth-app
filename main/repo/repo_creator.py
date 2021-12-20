from .user_repo import _UserRepository
from .user_token_repo import _TokenRepository


def get_user_token_repo() -> _TokenRepository:
    return _TokenRepository.get_instance()


def get_user_repo() -> _UserRepository:
    return _UserRepository.get_instance()



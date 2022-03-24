from typing import List


class UserData:
    userId: int = None
    privileges: List[str] = None

    def __init__(self, user_id: int, privileges: List[str]):
        self.userId = user_id
        self.privileges = privileges

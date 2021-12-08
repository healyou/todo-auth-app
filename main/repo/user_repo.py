class User:
    id = 1
    public_id = 11
    name = "1"
    email = "1@mail.com"
    # password = "password"
    psw_hash = '$2b$10$VYrUvPcb4DuOEOcSgtPlC.8Im3CpXBFU7kFWkvhofnVGVIZaSkEpy'

    def __init__(self):
        pass


# TODO начитка юзеров из другого приложения
class UserRepository:
    users = {}

    def __init__(self):
        user = User()
        self.users[user.name] = user

    def get_by_username(self, username):
        return self.users.get(username)


import bcrypt


class HashProvider:
    salt = None

    def __init__(self):
        self.salt = 10
        pass

    def hash_psw(self, psw):
        return bcrypt.hashpw(psw.encode('utf-8'), bcrypt.gensalt(self.salt))

    def check_psw(self, psw, hash_psw):
        return bcrypt.checkpw(psw.encode('utf-8'), hash_psw.encode('utf-8'))


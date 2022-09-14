from flask_login import UserMixin

user_role_map = {
    '58691426': 'writer'
}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def getRole(self):
        return user_role_map.get(self.id, 'reader')

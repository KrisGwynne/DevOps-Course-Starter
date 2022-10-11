from flask_login import UserMixin, AnonymousUserMixin

user_role_map = {
    '58691426': 'writer'
}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_role(self):
        return user_role_map.get(self.id, 'reader')

class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        pass
    
    def get_role(self):
        return 'writer'

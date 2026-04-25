class HBnBFacade:
    def __init__(self):
        self.users = []

    # ---------- USERS ----------
    def create_user(self, data):
        self.users.append(data)
        return data

    def get_all_users(self):
        return self.users

    def get_user(self, user_id):
        for user in self.users:
            if user["id"] == user_id:
                return user
        return None

    def update_user(self, user_id, data):
        for user in self.users:
            if user["id"] == user_id:
                user.update(data)
                return user
        return None

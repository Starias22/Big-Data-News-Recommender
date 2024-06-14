from pymongo import MongoClient
from profiles.user import User

class UserDB:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def save_user(self, user):
        user_dict = user.to_dict()
        result = self.db.users.insert_one(user_dict)
        return result.inserted_id

    def find_user_by_id(self, user_id):
        user_data = self.db.users.find_one({"id": user_id})
        if user_data:
            return User.from_dict(user_data)
        return None

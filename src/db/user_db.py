from pymongo import MongoClient
from profiles.user import User

class UserDB:
    def __init__(self,uri="mongodb://localhost:27017/",db_name="news_recommendation_db"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def create_user(self, user):
        user_dict = user.to_dict()
        result = self.db.users.insert_one(user_dict)
        return result.inserted_id

    def find_user_by_id(self, user_id):
        user_data = self.db.users.find_one({"id": user_id})
        if user_data:
            return User.from_dict(user_data)
        return None
    
    def find_user_by_email(self, user_email):
        user_data = self.db.users.find_one({"email": user_email})
        if user_data:
            print("user_data:",user_data)
            return User.from_dict(user_data)
        return None
    
    def retrieve_user_preferences(self):
        users = self.db.users.find()
        return [User.retrieve_preferences(user_data) for user_data in users]

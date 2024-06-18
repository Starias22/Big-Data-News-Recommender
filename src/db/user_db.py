from pymongo import MongoClient
import sys
from pathlib import Path
# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[1]
sys.path.append(str(src_path))

from models.user import User
from utils import encrypt_password
from typing import Optional
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
    
    def find_user_by_email(self, user: User):
        user_data = self.db.users.find_one({"email": user.email})
        if user_data:
            return User.from_dict(user_data)
        return None
    
    def authenticate(self, user: User) ->Optional[User]:
        print(encrypt_password(user.password))
        user_data = self.db.users.find_one({"email":user.email ,
        
                                            "password":encrypt_password(user.password)})
        if user_data:
            return User.from_dict(user_data)
        return None
    
    def retrieve_user_preferences(self):
        users = self.db.users.find()
        return [User.retrieve_preferences(user_data) for user_data in users]

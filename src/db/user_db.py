from bson import ObjectId
from pymongo import MongoClient
import sys
from pathlib import Path
# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[1]
sys.path.append(str(src_path))

from models.user import User
from utils import encrypt_password
from typing import Dict, Optional
class UserDB:
    def __init__(self,uri="mongodb://localhost:27017/",db_name="news_recommendation_db"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def create_user(self, user):
        user_dict = user.to_dict()
        result = self.db.users.insert_one(user_dict)
        id=result.inserted_id
        user=self.find_user_by_id(id)
        user.display()
        return user

    def find_user_by_id(self, user_id):
        print('User id is',user_id)
        user_data = self.db.users.find_one({"_id": ObjectId(user_id)})
        print('User data is',user_data)

        if user_data:
            return User.from_dict(user_data)
        return None
    
    def find_user_by_email(self,  email):
        user_data = self.db.users.find_one({"email": email})
        print('user data is',user_data)
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
    
    def retrieve_user_ids(self):
        users = self.db.users.find()
        return [User.retrieve_id(user_data).id for user_data in users]

    def add_seen_news(self, user_id, news_actions):
        user = self.find_user_by_id(user_id)

        print('The user is')
        user.display()
        if user:
            user.add_seen_news(news_actions)
            print('The seen news are',user.seen_news)
            self.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"seen_news": user.seen_news}}
            )
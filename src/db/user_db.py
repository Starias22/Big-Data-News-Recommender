from bson import ObjectId
from pymongo import MongoClient
from typing import Dict, List, Optional
import sys
from pathlib import Path
# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))

from src.models.user import User
from src.utils import encrypt_password
from config.config import MONGO_DB_URI,MONGO_DB_NAME

class UserDB:
    def __init__(self,uri=MONGO_DB_URI,db_name=MONGO_DB_NAME):
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
    
    def retrieve_user_categories(self, user_id: str) -> Optional[List[int]]:
        user_data = self.db.users.find_one({"_id": ObjectId(user_id)})

        if user_data and 'categories' in user_data:
            print('++++++++++++++++++++++++++++++++++++=')
            print(user_data['categories'])
            return user_data['categories']
        return None
    
    def retrieve_user_sentiments(self, user_id: str) -> Optional[List[int]]:
        user_data = self.db.users.find_one({"_id": ObjectId(user_id)})

        if user_data and 'sentiments' in user_data:
            print('++++++++++++++++++++++++++++++++++++=')
            print(user_data['sentiments'])
            return user_data['sentiments']
        return None

    def add_category_to_user(self, user_id: str, category_id: int):
        user = self.find_user_by_id(user_id)

        if user:
            
           

            if category_id not in user.categories:
                user.categories.append(category_id)

                self.db.users.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"categories": user.categories}}
                )

    def remove_category_from_user(self, user_id: str, category_id: int):
        user = self.find_user_by_id(user_id)
        if category_id in user.categories:
            user.categories.remove(category_id)

            self.db.users.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"categories": user.categories}}
                )
            
    def update_sentiments(self, user_id: str, sentiments: List):
        #user = self.find_user_by_id(user_id)

        self.db.users.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"sentiments": sentiments}}
                )

# Usage example:
if __name__ == "__main__":
    user_db = UserDB()

    # Add category to user
    user_id = "6692f7bdfecf94edfeccafa1"  # Replace with actual user ID
    category_id_to_add = 1  # Replace with actual category ID
    #user_db.add_category_to_user(user_id, category_id_to_add)

    # Remove category from user
    category_id_to_remove = 1  # Replace with actual category ID to remove
    user_db.remove_category_from_user(user_id, category_id_to_remove)
from pymongo import MongoClient
from src.profiles.user_preference import UserPreference

class UserPreferenceDB:
    def __init__(self, uri, db_name="news_recommendation_db"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def save_user_preference(self, user_preference):
        user_preference_dict = user_preference.to_dict()
        result = self.db.user_preferences.insert_one(user_preference_dict)
        return result.inserted_id

    def find_user_preference_by_id(self, user_id):
        user_preference_data = self.db.user_preferences.find_one({"id": user_id})
        if user_preference_data:
            return UserPreference.from_dict(user_preference_data)
        return None

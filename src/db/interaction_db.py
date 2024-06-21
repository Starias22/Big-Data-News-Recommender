from typing import Dict
from pymongo import MongoClient
from pathlib import Path
import sys

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))
from src.models.interaction import Interaction
from config.config import MONGO_DB_NAME,MONGO_DB_URI

class InteractionDB:
    def __init__(self, uri=MONGO_DB_URI, db_name=MONGO_DB_NAME):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db.interactions  # Access the interactions collection

    def insert_interaction(self, interaction):
        interaction_dict = interaction.to_dict_persist()
        result = self.collection.insert_one(interaction_dict)
        return result.inserted_id

    def create_interaction(self, interaction):
        interaction_dict = interaction.to_dict()
        result = self.db.interactions.insert_one(interaction_dict)
        return result.inserted_id

    def find_interaction_by_id(self, interaction_id):
        interaction_data = self.db.interactions.find_one({"id": interaction_id})
        if interaction_data:
            return Interaction.from_dict(interaction_data)
        return None

    def find_interaction_by_user_id(self, user_id):
        interaction_data = self.db.interactions.find({"user_id": user_id})
        if interaction_data:
            return [Interaction.from_dict(data) for data in interaction_data]
        return None

    def retrieve_all_interactions(self, seen_and_liked_news_ids=None):
        interactions = self.db.interactions.find()
        interaction_list = [Interaction.from_dict(interaction_data) for interaction_data in interactions]
        print(interaction_list)
        if seen_and_liked_news_ids is not None:
            interaction_list = [interaction for interaction in interaction_list if interaction.news_id in seen_and_liked_news_ids]
        
        return interaction_list

    def update_interaction(self, interaction_id, update_fields):
        result = self.db.interactions.update_one(
            {"id": interaction_id},
            {"$set": update_fields}
        )
        return result.modified_count

    def delete_interaction(self, interaction_id):
        result = self.db.interactions.delete_one({"id": interaction_id})
        return result.deleted_count

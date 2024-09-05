#user.py
"""This modules contains functions to manage users"""
from pathlib import Path
from datetime import datetime
import sys
from src.utils import encrypt_password, is_empty

#from typing import Dict
# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[1]
sys.path.append(str(src_path))

class User:
    """This class defines methods for user management"""
    # pylint: disable=too-many-instance-attributes, too-many-arguments
    def __init__(self, user_id=None, firstname=None, lastname=None, email=None,password=None,
                categories= None,
                sentiments= None,
                seen_news= None,
                ansa=True,creation_date=int(datetime.now().timestamp()),
                recommended_news=None):
        self.id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.categories = categories if categories is not None else [1, 5, 7, 8, 10, 11]
        self.sentiments = sentiments if sentiments is not None else [0, -1, 1]
        self.seen_news = seen_news if seen_news is not None else []
        self.ansa=ansa
        self.password=password
        self.creation_date=creation_date
        self.recommended_news = recommended_news if recommended_news is not None else []

    def to_dict(self):
        """This method converts a user to a Python dictionary"""
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "password":encrypt_password(self.password),
            "creation_date":self.creation_date,
            "categories": self.categories,
            "sentiments": self.sentiments,
            "seen_news": self.seen_news,
            "ansa":self.ansa,                
        }

    @staticmethod
    def from_dict(data):
        """This method return the user that matches the given Python dictionay"""
        return User(
            user_id=str(data.get('_id')),
            firstname=data.get('firstname'),
            lastname=data.get('lastname'),
            email=data.get('email'),
            categories=data.get('categories'),
            sentiments=data.get('sentiments'),
            seen_news=data.get('seen_news'),
            ansa=data.get('ansa'),
            recommended_news=data.get("recommended_news")
        )

    @staticmethod
    def retrieve_preferences(data):
        """This method retrieves user preferences"""
        return User(
            user_id=data.get('_id'),
            categories=data.get('categories'),
            sentiments=data.get('sentiments'),
            seen_news=data.get('seen_news'),
            ansa=data.get('ansa'),
            email=data.get('email'),
        )

    @staticmethod
    def retrieve_id(data):
        """This method retrieves id"""
        return User(
            user_id=str(data.get('_id'))

        )

    def display(self):
        """This method displays key informations on user"""
        print('Firstname:', self.firstname)
        print('Lastname:', self.lastname)
        print('Email:', self.email)
        print('Password:', self.password)
        print('seen news',self.seen_news)

    def is_empty(self,authentication=False):
        """This method is used during user registration process. 
        It checks if a user missing email or password"""
        self.display()
        if authentication:
            return is_empty(self.email) or is_empty( self.password)

        # Check if any required fields are empty or None
        return  is_empty(self.firstname) or \
                is_empty(self.lastname) or \
                is_empty(self.email) or \
                is_empty( self.password)

    def add_seen_news(self, news_actions):
        """This method takes some news action and addthem to the seen news list in 
        the current user's document"""
        existing_news_ids = {list(news.keys())[0] for news in self.seen_news}
        for news_id, action in news_actions.items():
            if news_id not in existing_news_ids:
                self.seen_news.append({news_id: action})

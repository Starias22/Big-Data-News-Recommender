from datetime import datetime
from pymongo import MongoClient
import sys
from pathlib import Path
# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[1]
sys.path.append(str(src_path))

from utils import encrypt_password,is_empty

class User:
    def __init__(self, id=None, firstname=None, lastname=None, email=None,password=None,
                 categories=[i for i in range(32)], sentiments=[0,-1,1], seen_news=[],
                 ansa=True,creation_date=datetime.now(),recommended_news=[]):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.categories = categories
        self.sentiments = sentiments
        self.seen_news = seen_news 
        self.ansa=ansa
        self.password=password
        self.creation_date=creation_date
        self.recommended_news=recommended_news
        

    def to_dict(self):
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
        return User(
            #id=data.get('_id'),
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            categories=data.get('categories'),
            sentiments=data.get('sentiments'),
            seen_news=data.get('seen_news'),
            ansa=data.get('ansa'),
            recommended_news=data.get("recommended_news")
            

        )

    @staticmethod
    def retrieve_preferences(data):
        return User(
            #id=data.get('_id'),
            categories=data.get('categories'),
            sentiments=data.get('sentiments'),
            seen_news=data.get('seen_news'),
            ansa=data.get('ansa'),
            email=data.get('email'),

        )

    def display(self):
        print('Firstname:', self.firstname)
        print('Lastname:', self.lastname)
        print('Email:', self.email)
        print('Password:', self.password)

    def is_empty(self,authentication=False):
        self.display()
        if authentication==True:
            return is_empty(self.email) or is_empty( self.password)

        # Check if any required fields are empty or None
        return is_empty(self.firstname) or is_empty(self.lastname) or is_empty(self.email) or is_empty( self.password)
          
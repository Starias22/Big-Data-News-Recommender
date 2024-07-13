# src/controllers/welcome_controller.py
from src.models.user import User
from src.db.user_db import UserDB
from src.utils import generate_otp,send_email
from src.consumers.recommended_news_fetcher import fetch_recommended_news
from utils import is_empty
from src.producers.interactions_producer import send_interaction
#from src.db.interaction_db import InteractionDB
from src.models.interaction import Interaction
from datetime import datetime
#ezechieladede@gmail.com
import re
from typing import Optional
class WelcomeController:
    def __init__(self,email=None,password=None,firstname=None,lastname=None,password_confirm=None):
        self.user_db=UserDB()
        self.user=User(email=email,
                       password=password,
                       firstname=firstname,
                       lastname=lastname)
        
        self.password_confirm=password_confirm

    def login(self) ->Optional[User]:
        if self.user.is_empty(authentication=True):
            return 1
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Validate the email address
        if not re.match(email_regex, self.user.email):
            return 2  # Invalid email address
        user=self.user_db.authenticate(self.user)
        
        if user is None:
            return None
        #print('The user is')
        #user.display()
        return user
        

    def valid_new_user(self):

        if  self.user.is_empty() or is_empty(self.password_confirm):
            return 1
        # Define a regex pattern for validating email addresses
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Validate the email address
        if not re.match(email_regex, self.user.email):
            return 2  # Invalid email address
        if len(self.user.password)<6:
            return 3
        if self.password_confirm!=self.user.password:
            return 4
        if self.user_db.find_user_by_email(self.user.email) :
            return 5 # Email add already in use
        
        #self.user_db.create_user(self.user)
        return 0
    
    def send_verification_email(self):
        otp =generate_otp()
        body = f'Your 6-digit verification code is: {otp}'
        sent=send_email(receiver_addr=self.user.email,subject="Email verification",body=body)
        if sent:
            return otp
        return 1

    def register(self):
        user=self.user_db.create_user(self.user)
    
        return user.email


    def get_recommended_news(self,user_id):
        self.user.display()
        print(self.user.email)
        print(self.user.id)
        recommended_news=fetch_recommended_news(user_id=user_id)
        recommended_news=[news.to_dict() for news in recommended_news]
        #print('The first recommended news is:')
        #print(recommended_news[0])
        
        
        return recommended_news

    def register_interaction(self,user_id,news_id,action):
        interaction=Interaction(user_id=user_id,news_id=news_id,action=action,date=int(datetime.now().timestamp()))
        send_interaction(interaction)


    def get_user_categories(self, user_id):
            # Fetch user categories from database or return an empty list
            return self.user_db.retrieve_user_categories(user_id=user_id)
            

    def add_user_category(self, user_id, category):
        self.user_db.add_category_to_user(user_id=user_id,category_id=category)

        # Add a new category for the user in the database
        

    def remove_user_category(self, user_id, category):
        # Remove a category for the user from the database
        self.user_db.remove_category_from_user(user_id=user_id,category_id=category)

    def get_user_sentiments(self, user_id):
        # Fetch user sentiments from database or return an empty list
        return []

    def add_user_sentiment(self, user_id, sentiment):
        # Add a new sentiment for the user in the database
        pass

    def remove_user_sentiment(self, user_id, sentiment):
        # Remove a sentiment for the user from the database
        pass



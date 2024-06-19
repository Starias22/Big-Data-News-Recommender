# src/controllers/welcome_controller.py
from src.models.user import User
from src.db.user_db import UserDB
from src.utils import generate_otp,send_email
from src.consumers.recommended_news_fetcher import fetch_recommended_news
import re
from typing import Optional
class WelcomeController:
    def __init__(self,email=None,password=None,firstname=None,lastname=None):
        self.user_db=UserDB()
        self.user=User(email=email,
                       password=password,
                       firstname=firstname,
                       lastname=lastname)
        
    

    def login(self) ->Optional[User]:
        if self.user.is_empty(authentication=True):
            return 1
        user=self.user_db.authenticate(self.user)
        
        if user is None:
            return None
        print('The user is')
        user.display()
        return user
        

    def valid_new_user(self):

        if  self.user.is_empty():
            return 1
        # Define a regex pattern for validating email addresses
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Validate the email address
        if not re.match(email_regex, self.user.email):
            return 2  # Invalid email address
        if self.user_db.find_user_by_email(self.user.email) :
            return 3 # Email add already in use
        
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


    def get_recommended_news(self):
        self.user.display()
        print(self.user.email)
        print(self.user.id)
        recommended_news=fetch_recommended_news(user_email=self.user.email)
        recommended_news=[news.to_dict() for news in recommended_news]
        print(recommended_news)
        
        
        return recommended_news
        

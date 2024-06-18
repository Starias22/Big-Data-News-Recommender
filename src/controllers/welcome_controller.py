# src/controllers/welcome_controller.py
from src.models.user import User
from src.db.user_db import UserDB
from src.utils import is_empty
import re
from typing import Optional
class WelcomeController:
    def __init__(self,email,password,firstname=None,lastname=None):
        self.user_db=UserDB()
        self.user=User(email=email,
                       password=password,
                       firstname=firstname,
                       lastname=lastname)
        
    

    def login(self) ->Optional[User]:
        if self.user.is_empty(authentication=True):
            return 1
        return self.user_db.authenticate(self.user)
        

    def register(self):

        if  self.user.is_empty():
            return 1
        # Define a regex pattern for validating email addresses
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Validate the email address
        if not re.match(email_regex, self.user.email):
            return 2  # Invalid email address
        if self.user_db.find_user_by_email(self.user) :
            return 3 # Email add already in use
        
        self.user_db.create_user(self.user)
        return 0
        

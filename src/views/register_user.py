import streamlit as st
import sys
import os
from pathlib import Path
#src_path = Path(__file__).resolve().parents[2] 
#print(src_path)
#sys.path.append(os.path.join(os.path.dirname(__file__),'models'))

from ..models.user import User
from db.user_db import UserDB
#from src.profiles.user import User


# Streamlit app
st.title("News Recommendation System")


# Add a new user
st.header("Register")
firstname = st.text_input("Firstname")
lastname = st.text_input("Lastname")
email = st.text_input("Email")
password=st.text_input("Password",type="password")


if st.button("Add User"):
    new_user=User(firstname=firstname,
              lastname=lastname,
              email=email,
              password=password)
    user_db=UserDB()
    user_db.create_user(user=new_user)
    st.success("User added successfully!")




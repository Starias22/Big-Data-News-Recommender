# src/views/welcome_page.py
import streamlit as st
from src.controllers.welcome_controller import WelcomeController

def show_welcome_page():
    

    # Set up the homepage title and subtitle
    st.title('Welcome to Big Data News Recommendation App')
    st.subheader('Get personalized news based on the latest big data trends.')

    # Introduction text
    st.write("""
    Welcome to the Big Data News Recommendation App! Here, you'll find the most relevant and up-to-date news articles tailored to your interests using cutting-edge big data technology. 
    Register or log in to start receiving personalized news recommendations right away!
    """)

    # Tabs for Login and Registration
    tab = st.radio("Choose an option:", ["Login", "Register"])

    if tab == "Login":
        st.header('Login')
        login_email = st.text_input('Email', key='login_email')
        login_password = st.text_input('Password', type='password', key='login_password')
        
        if st.button('Login'):
            controller = WelcomeController(email=login_email,
                                           password=login_password)
            user = controller.login()
                
            if user==1:
                st.error('Please fill in both the email and password fields.')
            
            elif user is None:
                    st.error('Email or password incorrect.')
            elif user:
                st.success(f'Welcome back, {user.firstname}!')
                
            else:
                st.error('Unknown error.')
            
    else:
        st.header('Register')
        register_firstname = st.text_input('Firstname', key='register_firstname')
        register_lastname = st.text_input('Lastname', key='register_lastname')

        register_email = st.text_input('Email', key='register_email')
        register_password = st.text_input('Password', type='password', key='register_password')
        
        if st.button('Register'):

            controller = WelcomeController(firstname=register_firstname,
                                           lastname=register_lastname,
                                           email=register_email,
                                           password=register_password)
           
            
            reg_code = controller.register()
            if reg_code==1:
                st.error('Please fill in all the fields.')
            elif reg_code==2:
                st.error('Invalid emai address.')
            
            elif reg_code==3:
                st.error('Emai address already in use!')

            elif reg_code==0:
                st.success(f'Thank you for registering, {register_firstname}! We have sent a confirmation email to your address.')

            else:
                st.error('Unkown error.')

    # Footer with additional information
    st.markdown("---")
    st.markdown("""
    ### About Us
    The Big Data News Recommendation App uses advanced algorithms and machine learning techniques to curate news articles that match your interests and preferences.

    ### Contact Us
    If you have any questions, feel free to reach out to us at support@bigdatanewsapp.com.
    """)

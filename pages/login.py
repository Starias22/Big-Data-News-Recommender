import streamlit as st
from src.controllers.welcome_controller import WelcomeController
from config.config import SENDER_ADDRESS
from streamlit_extras.switch_page_button import switch_page


def show_welcome_page():
    # Check if the user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

    # If logged in, show recommended news
    if st.session_state.logged_in:
        #st.header('Recommended News')
        #controller = WelcomeController(email=st.session_state.user_email)
        #show_recommended_news(controller)
        switch_page("news")

    else:
        
        # Direct Login Form
        st.header('Login')
        with st.form("login_form"):
            login_email = st.text_input('Email', key='login_email').strip()
            login_password = st.text_input('Password', type='password', key='login_password').strip()
            login_button = st.form_submit_button('Login')

            if login_button:
                controller = WelcomeController(email=login_email, password=login_password)
                user = controller.login()
                
                if user == 1:
                    st.error('Please fill in both the email and password fields.')
                elif user == 2:
                    st.error('Invalid email address.')
                elif user is None:
                    st.error('Email or password incorrect.')
                elif user:
                    st.session_state.logged_in = True
                    st.session_state.user_email = user.email
                    st.session_state.user_id = user.id
                    st.success(f'Welcome back, {user.firstname}!')
                    st.rerun()
                else:
                    st.error('Unknown error.')

        # Footer with additional information
        

if __name__ == "__main__":
    show_welcome_page()

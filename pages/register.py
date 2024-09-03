import streamlit as st
from src.controllers.welcome_controller import WelcomeController
from streamlit_extras.switch_page_button import switch_page

from config.config import SENDER_ADDRESS

def show_welcome_page():
    # Initialize session state for registration
    if 'registration_complete' not in st.session_state:
        st.session_state.registration_complete = False
    if 'otp' not in st.session_state:
        st.session_state.otp = -1
    if 'user_registered' not in st.session_state:
        st.session_state.user_registered = False
    if 'register_details' not in st.session_state:
        st.session_state.register_details = {}

    # Registration Form
    if not st.session_state.registration_complete and not st.session_state.user_registered:
        with st.form("register_form"):
            st.header('Register')
            register_firstname = st.text_input('Firstname', key='register_firstname').strip()
            register_lastname = st.text_input('Lastname', key='register_lastname').strip()
            register_email = st.text_input('Email', key='register_email').strip()
            register_password = st.text_input('Password', type='password', key='register_password').strip()
            register_password_confirm = st.text_input('Confirm password', type='password', key='register_password_confirm').strip()
            register_button = st.form_submit_button('Register')

            if register_button:
                controller = WelcomeController(
                    firstname=register_firstname,
                    lastname=register_lastname,
                    email=register_email,
                    password=register_password,
                    password_confirm=register_password_confirm
                )
                
                reg_code = controller.valid_new_user()
                if reg_code == 1:
                    st.error('Please fill in all the fields.')
                elif reg_code == 2:
                    st.error('Invalid email address.')
                elif reg_code == 3:
                    st.error('At least 6 characters required for password!')
                elif reg_code == 4:
                    st.error('The two passwords do not match!')
                elif reg_code == 5:
                    st.error('Email address already in use!')
                elif reg_code == 0:
                    otp = controller.send_verification_email()
                    if otp == 1:
                        st.error('Email not sent! Are you sure your email address is correct?')
                    else:
                        st.session_state.otp = otp
                        st.session_state.registration_complete = True
                        st.session_state.register_details = {
                            "firstname": register_firstname,
                            "lastname": register_lastname,
                            "email": register_email,
                            "password": register_password
                        }
                        st.success(f'Thank you, {register_firstname}! A 6-digit confirmation code has been sent to your email address.')
                else:
                    st.error('Unknown error.')

    # OTP Verification Form
    if st.session_state.registration_complete and not st.session_state.user_registered:
        with st.form("verification_form"):
            confirmation_code = st.text_input('Enter the 6-digit confirmation code', key='confirmation_code')
            verify_button = st.form_submit_button('Verify Code')

            if verify_button:
                if str(st.session_state.otp) == str(confirmation_code):
                    # Initialize controller again with registration details
                    register_details = st.session_state.register_details
                    controller = WelcomeController(
                        firstname=register_details["firstname"],
                        lastname=register_details["lastname"],
                        email=register_details["email"],
                        password=register_details["password"]
                    )
                    st.session_state.user_id = controller.register()
                    st.success(f'Registration completed! Your email has been verified successfully, {register_details["firstname"]}!')
                    st.session_state.logged_in = True
                    switch_page("login")

                    # Mark user as registered to prevent re-registration
                    st.session_state.user_registered = True

                    # Clear registration state
                    st.session_state.registration_complete = False
                    st.session_state.otp = -1
                    st.session_state.register_details = {}

                else:
                    st.error('Incorrect confirmation code. Please try again.')

    # Display message if user is already registered
    if st.session_state.user_registered:
        st.success(f'You are already registered and logged in.')

if __name__ == "__main__":
    show_welcome_page()

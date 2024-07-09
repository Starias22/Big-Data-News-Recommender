import streamlit as st
from src.controllers.welcome_controller import WelcomeController
from config.config import SENDER_ADDRESS
from src.utils import format_duration,format_source
from src.views.settings_page import show_settings_page 

import webbrowser
from config.config import DISLIKED,SEEN,LIKED

def log_interaction_and_open_link(user_id, news_id, action, url):
    WelcomeController().register_interaction(user_id=user_id, news_id=news_id, action=action)
    js = f"window.open('{url}');"
    html = f"<script>{js}</script>"
    st.markdown(html, unsafe_allow_html=True)

def log_interaction(user_id, news_id, action):
    WelcomeController().register_interaction(user_id=user_id, news_id=news_id, action=action)


def show_recommended_news(controller):
    # Fetch recommended news based on user_id using the controller
    recommended_news = controller.get_recommended_news(user_id=st.session_state.user_id)
    print('****************************************************')
    print(recommended_news)
    for news in recommended_news:
        st.write(news['category'])
        
        if news['img_url'] is not None:  # Check if the image URL is not None
            # Use HTML and CSS to center the image
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <img src="{news['img_url']}" alt="" style="max-width: 100%;">
                </div>
                """, unsafe_allow_html=True
            )
        #st.write(f'***{news["title"]}***')
        st.markdown(
    f"""
    <h3 style='text-align: center;'>
        {news['title']}
    </h3>
    """,
    unsafe_allow_html=True
)

        # Display news details with icons aligned to the right
        col1, col2, col3, col4, col5 = st.columns([8, 1, 1, 1, 1])
        
        with col1:
            st.write(f"{format_source(news['source_name'],news['author'])} {format_duration(news['publication_date'])}")
        with col2:
            
            if st.button(f"👁️", key=f"view_{news['_id']}"):
                webbrowser.open(news['url'])
                print(f"Title clicked: {news['title']}")
                print('You are the user',st.session_state.user_id)
                
                WelcomeController().register_interaction(user_id=st.session_state.user_id,
                                                news_id=news['_id'],action=SEEN)

        with col3:
            if st.button('👍', key=f"like_{news['_id']}"):
                WelcomeController().register_interaction(user_id=st.session_state.user_id,
                                                news_id=news['_id'],action=LIKED)
        
        with col4:
            if st.button('👎', key=f"dislike_{news['_id']}"):
                WelcomeController().register_interaction(user_id=st.session_state.user_id,
                                                news_id=news['_id'],action=DISLIKED)

        

        with col5:
            if st.button('⋮', key=f"menu_{news['_id']}"):
                pass
                #st.session_state[f"menu_{news['_id']}"] = True
                
        # Check session state for button clicks
        #if st.session_state.get(f"view_{news['_id']}"):
            #print(f"Title clicked: {news['title']}")
            #st.session_state[f"view_{news['_id']}"] = False  # Reset state

        st.write(news['sentiment_score'])

        # Separator
        st.markdown("---")


def show_welcome_page():
    # Check if the user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'registration_complete' not in st.session_state:
        st.session_state.registration_complete = False
    if 'otp' not in st.session_state:
        st.session_state.otp = -1

    # If logged in, show recommended news
    if st.session_state.logged_in:
        if st.button('Manage Preferences'):  # Example button for navigating to settings page
            show_settings_page(WelcomeController())

        st.header('Recommended News')
        controller = WelcomeController(email=st.session_state.user_email)
        show_recommended_news(controller)
    else:
        # Set up the homepage title and subtitle
        st.title('Welcome to Big Data News Recommendation App')
        st.subheader('Get news articles based on your preferences')

        # Introduction text
        st.write("""
        Welcome to the Big Data News Recommendation App! Here, you'll find the most relevant and up-to-date news articles tailored to your interests using cutting-edge big data technology. 
        Register or log in to start receiving personalized news recommendations right away!
        """)

        # Tabs for Login and Registration
        tab = st.radio("Choose an option:", ["Login", "Register"])

        if tab == "Login":
            with st.form("login_form"):
                st.header('Login')
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
                        print('The user id is',user.id)
                        st.success(f'Welcome back, {user.firstname}!')
                        st.rerun()
                    else:
                        st.error('Unknown error.')
                
        else:
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
                            st.success(f'Thank you, {register_firstname}! A 6-digit confirmation code has been sent to your email address.')
                    else:
                        st.error('Unknown error.')

            if st.session_state.registration_complete:
                with st.form("verification_form"):
                    confirmation_code = st.text_input('Enter the 6-digit confirmation code', key='confirmation_code')
                    verify_button = st.form_submit_button('Verify Code')
                    
                    if verify_button:
                        print(confirmation_code)
                        if str(st.session_state.otp) == str(confirmation_code):
                            # Initialize controller again with registration details
                            controller = WelcomeController(
                                firstname=register_firstname,
                                lastname=register_lastname,
                                email=register_email,
                                password=register_password
                            )
                            st.session_state.user_email = controller.register()
                            st.success(f'Registration completed! Your email has been verified successfully, {register_firstname}!')
                            st.session_state.logged_in = True
                            st.rerun()
                        else:
                            st.error('Incorrect confirmation code. Please try again.')
        
        # Footer with additional information
        st.markdown("---")
        st.markdown("""
        ### About Us
        The Big Data News Recommendation App uses advanced algorithms and machine learning techniques to curate news articles that match your interests and preferences.

        ### Contact Us
        If you have any questions, feel free to reach out to us at {}.
        """.format(SENDER_ADDRESS))

if __name__ == "__main__":
    show_welcome_page()

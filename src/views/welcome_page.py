import streamlit as st
from src.controllers.welcome_controller import WelcomeController

def show_recommended_news(controller):
    # Fetch recommended news based on user_id using the controller
    recommended_news = controller.get_recommended_news()

    # Display recommended news
    for news in recommended_news:
        st.write(f"**{news['title']}**")
        st.write(news['description'])
        st.write(news['category'])
        st.write(news['publication_date'])
        

        st.write(news['source_name'])
        st.write(news['author'])
        st.write(news['url'])
        st.write(news['img_url'])

        st.markdown("---")

def show_welcome_page():
    # Check if the user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

    # If logged in, show recommended news
    if st.session_state.logged_in:
        st.header('Recommended News')
        controller = WelcomeController()
        show_recommended_news(controller)
    else:
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
                controller = WelcomeController(email=login_email, password=login_password)
                user = controller.login()
                
                if user == 1:
                    st.error('Please fill in both the email and password fields.')
                elif user is None:
                    st.error('Email or password incorrect.')
                elif user:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user.id
                    st.success(f'Welcome back, {user.firstname}!')
                    st.rerun()
                else:
                    st.error('Unknown error.')
                
        else:
            st.header('Register')
            register_firstname = st.text_input('Firstname', key='register_firstname')
            register_lastname = st.text_input('Lastname', key='register_lastname')
            register_email = st.text_input('Email', key='register_email')
            register_password = st.text_input('Password', type='password', key='register_password')
            
            if st.button('Register'):
                controller = WelcomeController(
                    firstname=register_firstname,
                    lastname=register_lastname,
                    email=register_email,
                    password=register_password
                )
                
                reg_code = controller.register()
                if reg_code == 1:
                    st.error('Please fill in all the fields.')
                elif reg_code == 2:
                    st.error('Invalid email address.')
                elif reg_code == 3:
                    st.error('Email address already in use!')
                elif reg_code == 0:
                    st.success(f'Thank you for registering, {register_firstname}! We have sent a confirmation email to your address.')
                else:
                    st.error('Unknown error.')

        # Footer with additional information
        st.markdown("---")
        st.markdown("""
        ### About Us
        The Big Data News Recommendation App uses advanced algorithms and machine learning techniques to curate news articles that match your interests and preferences.

        ### Contact Us
        If you have any questions, feel free to reach out to us at Gbetoho.ADEDE@um6p.ma.com.
        """)


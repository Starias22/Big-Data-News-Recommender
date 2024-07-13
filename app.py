from src.views.welcome_page import show_welcome_page

def main():
    # Initially show the welcome page
    show_welcome_page()

    # Placeholder for additional logic after login/registration
    # Example: Show main app content if the user is logged in
    # if st.session_state.get('logged_in'):
    #     show_main_app()

if __name__ == "__main__":
    main()

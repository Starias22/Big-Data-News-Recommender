import streamlit as st

def show_welcome_page():
    # Set the title and subtitle for the welcome page
    st.title("Welcome to NewsEngine")
    st.subheader("Your personalized news recommendation system")

    # Add some introductory text
    st.write("""
    Discover the latest news articles tailored to your interests. 
    Sign in to get personalized recommendations or register to create an account.
    """)

    # Add some space before the buttons
    st.markdown("<br><br>", unsafe_allow_html=True)

    button_style = """
        <style>
        .stButton button {
            background-color: #007BFF;
            color: white;
            width: 80%;
            padding: 10px;
            font-size: 18px;
            margin: 10px 0;
        }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    if st.button('Login'):
        # Placeholder for login action
        st.session_state['login'] = True
        st.write("Login button clicked")

    if st.button('Register'):
        # Placeholder for register action
        st.session_state['register'] = True
        st.write("Register button clicked")

if __name__ == "__main__":
    show_welcome_page()

# settings_page.py (example)

import streamlit as st
from src.controllers.welcome_controller import WelcomeController


def show_settings_page(controller):
    st.title('User Preferences')
    
    # Fetch and display user categories
    st.header('Categories')
    user_categories = controller.get_user_categories(user_id=st.session_state.user_id)
    st.write(user_categories)
    
    # Add new category form
    new_category = st.text_input('New Category')
    add_category_button = st.button('Add Category')
    
    if add_category_button and new_category:
        controller.add_user_category(user_id=st.session_state.user_id, category=new_category)
        st.success(f'Category "{new_category}" added successfully!')
    
    # Display current categories and provide option to remove
    if user_categories:
        st.subheader('Current Categories')
        for category in user_categories:
            if st.button(f'Remove {category}', key=f'remove_{category}'):
                controller.remove_user_category(user_id=st.session_state.user_id, category=category)
                st.success(f'Category "{category}" removed!')
    
    # Fetch and display user sentiments
    st.header('Sentiments')
    user_sentiments = controller.get_user_sentiments(user_id=st.session_state.user_id)
    st.write(user_sentiments)
    
    # Add new sentiment form
    new_sentiment = st.text_input('New Sentiment')
    add_sentiment_button = st.button('Add Sentiment')
    
    if add_sentiment_button and new_sentiment:
        controller.add_user_sentiment(user_id=st.session_state.user_id, sentiment=new_sentiment)
        st.success(f'Sentiment "{new_sentiment}" added successfully!')
    
    # Display current sentiments and provide option to remove
    if user_sentiments:
        st.subheader('Current Sentiments')
        for sentiment in user_sentiments:
            if st.button(f'Remove {sentiment}', key=f'remove_{sentiment}'):
                controller.remove_user_sentiment(user_id=st.session_state.user_id, sentiment=sentiment)
                st.success(f'Sentiment "{sentiment}" removed!')

def main():
    # Initialize controller
    controller = WelcomeController()

    # Show the settings page
    show_settings_page(controller)

if __name__ == "__main__":
    main()

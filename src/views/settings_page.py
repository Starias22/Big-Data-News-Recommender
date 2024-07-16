import streamlit as st
from src.controllers.welcome_controller import WelcomeController
from config.config import CATEGORIES_MAPPING

def show_settings_page(controller):
    st.title('User Preferences')
    
    # Fetch user categories and category labels
    user_categories = controller.get_user_categories(user_id=st.session_state.user_id)
    user_category_labels = [CATEGORIES_MAPPING[cat_id] for cat_id in user_categories]
    all_categories = list(CATEGORIES_MAPPING.keys())
    
    # Compute other categories
    other_categories = [cat_id for cat_id in all_categories if cat_id not in user_categories]
    other_category_labels = [CATEGORIES_MAPPING[cat_id] for cat_id in other_categories]
    
    # Add columns for displaying categories side by side
    col1, col2 = st.columns(2)
    
    # Display user categories on the left
    with col1:
        st.header('Your Categories')
        for category_label in user_category_labels:
            remove_clicked = st.session_state.get(f'remove_{category_label}', False)
            if st.button(f'❌ {category_label}', key=f'remove_{category_label}'):
                st.session_state[f'remove_{category_label}'] = True
                remove_clicked = True
            
            if remove_clicked:
                category_id = next((k for k, v in CATEGORIES_MAPPING.items() if v == category_label), None)
                if category_id is not None:
                    controller.remove_user_category(user_id=st.session_state.user_id, category_id=category_id)
                    st.success(f'Category "{category_label}" removed!')
                    # Refresh user categories after removal
                    user_categories = controller.get_user_categories(user_id=st.session_state.user_id)
                    user_category_labels = [CATEGORIES_MAPPING[cat_id] for cat_id in user_categories]
    
    # Display all categories on the right
    with col2:
        st.header('Other Categories')
        for category_label in other_category_labels:
            add_clicked = st.session_state.get(f'add_{category_label}', False)
            if st.button(f'➕ {category_label}', key=f'add_{category_label}'):
                st.session_state[f'add_{category_label}'] = True
                add_clicked = True
            
            if add_clicked:
                category_id = next((k for k, v in CATEGORIES_MAPPING.items() if v == category_label), None)
                if category_id is not None:
                    controller.add_user_category(user_id=st.session_state.user_id, category_id=category_id)
                    st.success(f'Category "{category_label}" added successfully!')
                    # Refresh user categories after addition
                    user_categories = controller.get_user_categories(user_id=st.session_state.user_id)
                    user_category_labels = [CATEGORIES_MAPPING[cat_id] for cat_id in user_categories]
    
    # Fetch and display user sentiments
    st.header('Sentiments')
    user_sentiments = controller.get_user_sentiments(user_id=st.session_state.user_id)
    st.write(user_sentiments)
    
    # Add new sentiment form
    new_sentiment = st.text_input('New Sentiment')
    add_sentiment_button = st.button('Add Sentiment')
    
    if add_sentiment_button and new_sentiment:
        print(';;;;;;;;;;;;;;;;;;;;')

        controller.add_user_sentiment(user_id=st.session_state.user_id, sentiment=new_sentiment)
        st.success(f'Sentiment "{new_sentiment}" added successfully!')
    
    # Display current sentiments and provide option to remove
    if user_sentiments:
        st.subheader('Current Sentiments')
        for sentiment in user_sentiments:
            remove_sentiment_clicked = st.session_state.get(f'remove_{sentiment}', False)
            if st.button(f'Remove {sentiment}', key=f'remove_{sentiment}'):
                st.session_state[f'remove_{sentiment}'] = True
                remove_sentiment_clicked = True
            
            if remove_sentiment_clicked:
                controller.remove_user_sentiment(user_id=st.session_state.user_id, sentiment=sentiment)
                st.success(f'Sentiment "{sentiment}" removed!')

def main():
    # Initialize controller
    controller = WelcomeController()

    # Show the settings page
    show_settings_page(controller)

if __name__ == "__main__":
    main()

import streamlit as st
from src.controllers.welcome_controller import WelcomeController
from src.utils import format_duration, format_source
import webbrowser
from config.config import DISLIKED, SEEN, LIKED

def show_recommended_news(controller):
    # Fetch recommended news based on user_id using the controller
    recommended_news = controller.get_recommended_news(user_id=st.session_state.user_id)
    
    # Initialize session state for news display and pagination
    if 'news_displayed' not in st.session_state:
        st.session_state.news_displayed = []
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0
    
    # Pagination logic
    start_idx = st.session_state.page_number * 20
    end_idx = start_idx + 20
    current_news = recommended_news[start_idx:end_idx]
    
    for news in current_news:
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
            st.write(f"{format_source(news['source_name'], news['author'])} {format_duration(news['publication_date'])}")
        
        with col2:
            if st.button(f"👁️", key=f"view_{news['_id']}"):
                webbrowser.open(news['url'])
                WelcomeController().register_interaction(user_id=st.session_state.user_id, news_id=news['_id'], action=SEEN)

        with col3:
            if st.button('👍', key=f"like_{news['_id']}"):
                WelcomeController().register_interaction(user_id=st.session_state.user_id, news_id=news['_id'], action=LIKED)
        
        with col4:
            if st.button('👎', key=f"dislike_{news['_id']}"):
                WelcomeController().register_interaction(user_id=st.session_state.user_id, news_id=news['_id'], action=DISLIKED)

        with col5:
            if st.button('⋮', key=f"menu_{news['_id']}"):
                pass
                
        st.write(news['sentiment_score'])
        st.markdown("---")

    # Load more button logic
    if len(recommended_news) > end_idx:
        if st.button('Load More'):
            st.session_state.page_number += 1
            st.experimental_rerun()
    else:
        st.write("No more news to load.")

def show_welcome_page():
    # Check if the user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

    # If logged in, show recommended news
    if st.session_state.logged_in:
        st.header('Recommended News')
        controller = WelcomeController(email=st.session_state.user_email)
        show_recommended_news(controller)
    else:
        st.write("Please log in to see recommended news.")

if __name__ == "__main__":
    show_welcome_page()

from flask import Flask, render_template, request, redirect, url_for, flash, session
from src.controllers.welcome_controller import WelcomeController
from src.utils import format_duration, format_source
from config.config import CATEGORIES_MAPPING, POSITIVE_SENTIMENT, NEGATIVE_SENTIMENT, NEUTRAL_SENTIMENT
from config.messages import *
from src.utils import get_category_id
ERROR_MESSAGE_CATEGORY='error'
SUCCESS_MESSAGE_CATEGORY='success'
sentiment_scores = {
    'Positive': 1,
    'Negative': -1,
    'Neutral': 0
}


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

@app.route('/',methods=["GET"])
def home():
    # Not logged in, show welcome page
    if 'logged_in' not in session or not session['logged_in']:
        # Render the login page
        return render_template('index.html')
    else: # Already logged in, show recommended news
        return redirect(url_for('recommended_news'))
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    email=password=None
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']
        controller = WelcomeController(email=email, password=password)
        user = controller.login()
        if user == 1:
            flash(ERROR_MISSING_FIELDS, ERROR_MESSAGE_CATEGORY)
        elif user == 2:
            flash(ERROR_INVALID_EMAIL, ERROR_MESSAGE_CATEGORY)
        elif user is None:
            flash(ERROR_INCORRECT_CREDENTIALS, ERROR_MESSAGE_CATEGORY)
        elif user:
            session['user_id']=user.id
            session['logged_in'] = True
            flash(f'{SUCCESS_LOGIN}, {user.firstname}!', SUCCESS_MESSAGE_CATEGORY)
            return redirect(url_for('recommended_news'))
        else:
            flash(ERROR_UNKNOWN,ERROR_MESSAGE_CATEGORY)
    #if request.method == 'GET':
    if 'logged_in' not in session:
        # Render the login page for GET request
        return render_template('login.html', email=email, password=password)
    else:
        return redirect(url_for('recommended_news'))

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        # Clear all session data
        session.clear()
        flash(SUCCESS_LOGOUT, SUCCESS_MESSAGE_CATEGORY)
    return redirect(url_for('login'))

@app.route('/news-preferences', methods=['GET', 'POST'])
def news_preferences():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    controller = WelcomeController()
    
    if request.method == 'POST':
        if 'remove_category' in request.form:
            category_label = request.form['remove_category']
            category_id=get_category_id(label=category_label)
            controller.remove_user_category(user_id=session['user_id'], category_id=category_id)
            flash(SUCCESS_CATEGORY_REMOVED, SUCCESS_MESSAGE_CATEGORY)
        elif 'add_category' in request.form:
            
            category_label = request.form['add_category']
            category_id=get_category_id(label=category_label)

            controller.add_user_category(user_id=session['user_id'], category_id=category_id)
            flash(SUCCESS_CATEGORY_ADDED, SUCCESS_MESSAGE_CATEGORY)
        
        else:
            selected_sentiments = request.form.getlist('sentiments')
            new_sentiments=[]
            for selected_sentiment in selected_sentiments:
                new_sentiments.append(sentiment_scores[selected_sentiment])
            controller.update_user_sentiments(user_id=session['user_id'],sentiments=new_sentiments)

    # Fetch user categories and sentiments
    user_categories = controller.get_user_categories(user_id=session['user_id'])
    user_category_labels = [CATEGORIES_MAPPING[cat_id] for cat_id in user_categories]
    
    all_categories = list(CATEGORIES_MAPPING.keys())
    other_categories = [cat_id for cat_id in all_categories if cat_id not in user_categories]
    other_category_labels = [CATEGORIES_MAPPING[cat_id] for cat_id in other_categories]
    
    user_sentiments = controller.get_user_sentiments(user_id=session['user_id'])

    positive=negative=neutral=False
    if POSITIVE_SENTIMENT in user_sentiments:
        positive = True
    if NEGATIVE_SENTIMENT in user_sentiments:
        negative = True
    if NEUTRAL_SENTIMENT in user_sentiments:
        neutral = True

    return render_template('news_preferences.html', 
                           user_category_labels=user_category_labels,
                           other_category_labels=other_category_labels,
                           user_sentiments=user_sentiments,
                           positive=positive, negative=negative, 
                           neutral = neutral)



@app.route('/register', methods=['GET', 'POST'])
def register():
    email=password=None
    if request.method == 'POST':
        firstname = request.form.get('firstname').strip()
        lastname = request.form.get('lastname').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        password_confirm = request.form.get('password_confirm').strip()
        controller = WelcomeController(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password,
            password_confirm=password_confirm
        )
        reg_code = controller.valid_new_user()
        if reg_code == 1:
            flash(ERROR_MISSING_FIELDS, ERROR_MESSAGE_CATEGORY)
        elif reg_code == 2:
            flash(ERROR_INVALID_EMAIL, ERROR_MESSAGE_CATEGORY)
        elif reg_code == 3:
            flash(ERROR_WEAK_PASSWORD, ERROR_MESSAGE_CATEGORY)
        elif reg_code == 4:
            flash(ERROR_PASSWORD_MISMATCH, ERROR_MESSAGE_CATEGORY)
        elif reg_code == 5:
            flash(ERROR_EMAIL_IN_USE, ERROR_MESSAGE_CATEGORY)
        elif reg_code == 0:
            otp = controller.send_verification_email()
            if otp == 1:
                flash(ERROR_EMAIL_NOT_SENT, ERROR_MESSAGE_CATEGORY)
            else:
                session['otp'] = otp
                #session['registration_complete'] = True
                session['register_details'] = {
                    "firstname": firstname,
                    "lastname": lastname,
                    "email": email,
                    "password": password
                }
                flash(f'Thank you, {firstname}! A 6-digit confirmation code has been sent to your email address ({email}).', SUCCESS_MESSAGE_CATEGORY)
                return redirect(url_for('verify_otp'))
        else:
            flash(ERROR_UNKNOWN, ERROR_MESSAGE_CATEGORY)
    
    return render_template('register.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        confirmation_code = request.form.get('confirmation_code').strip()
        
        if str(session.get('otp')) == str(confirmation_code):
            register_details = session.get('register_details')
            controller = WelcomeController(
                firstname=register_details["firstname"],
                lastname=register_details["lastname"],
                email=register_details["email"],
                password=register_details["password"]
            )
            controller.register()
            flash(f'Registration completed! Your email has been verified successfully, {register_details["firstname"]}!', 'success')
            # Clear registration state
            #session.pop('registration_complete', None)
            session.pop('otp', None)
            session.pop('register_details', None)

            return redirect(url_for('login'))
        else:
            flash(WARNING_INVALID_OTP, ERROR_MESSAGE_CATEGORY)
    
    
    if 'register_details' in session :
            return render_template('verify_otp.html')
    else:
            return redirect(url_for('register'))

@app.route('/recommended-news')
def recommended_news():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    controller = WelcomeController()
    recommended_news = controller.get_recommended_news(user_id=session['user_id'])
    
    # Pagination logic
    page_number = int(request.args.get('page', 0))
    start_idx = page_number * 20
    end_idx = start_idx + 20
    current_news = recommended_news[start_idx:end_idx]

    return render_template('recommended_news.html', 
                           news=current_news, page_number=page_number, 
                           format_duration = format_duration, 
                           format_source = format_source)
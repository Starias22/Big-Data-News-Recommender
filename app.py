from flask import Flask, render_template, request, redirect, url_for, flash, session
from src.controllers.welcome_controller import WelcomeController
from src.utils import format_duration, format_source
from config.config import CATEGORIES_MAPPING
from config.messages import *
from src.utils import get_category_id
ERROR_MESSAGE_CATEGORY='error'
SUCCESS_MESSAGE_CATEGORY='success'

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

@app.route('/',methods=["GET"])
def home():
    if 'logged_in' not in session or not session['logged_in']:
        # Render the login page for GET request
        return render_template('index.html')
    else:
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
            #return str(category_id)
            controller.add_user_category(user_id=session['user_id'], category_id=category_id)
            flash(SUCCESS_CATEGORY_ADDED, SUCCESS_MESSAGE_CATEGORY)
        elif 'add_sentiment' in request.form:
            new_sentiment = request.form['new_sentiment']
            controller.add_user_sentiment(user_id=session['user_id'], sentiment=new_sentiment)
            flash(f'Sentiment added successfully!', SUCCESS_MESSAGE_CATEGORY)
        elif 'remove_sentiment' in request.form:
            sentiment = request.form['remove_sentiment']
            controller.remove_user_sentiment(user_id=session['user_id'], sentiment=sentiment)
            flash(f'Sentiment removed!', SUCCESS_MESSAGE_CATEGORY)
    
    
    # Fetch user categories and sentiments
    user_categories = controller.get_user_categories(user_id=session['user_id'])
    #return str(user_categories)
    #return CATEGORIES_MAPPING
    user_category_labels = [CATEGORIES_MAPPING[cat_id] for cat_id in user_categories]
    
    all_categories = list(CATEGORIES_MAPPING.keys())
    other_categories = [cat_id for cat_id in all_categories if cat_id not in user_categories]
    other_category_labels = [CATEGORIES_MAPPING[cat_id] for cat_id in other_categories]
    
    user_sentiments = controller.get_user_sentiments(user_id=session['user_id'])
    
    
    return render_template('news_preferences.html', 
                           user_category_labels=user_category_labels,
                           other_category_labels=other_category_labels,
                           user_sentiments=user_sentiments)



@app.route('/register', methods=['GET', 'POST'])
def register():
    print("Hello everyone")
    if request.method == 'POST':
        register_firstname = request.form.get('firstname').strip()
        register_lastname = request.form.get('lastname').strip()
        register_email = request.form.get('email').strip()
        register_password = request.form.get('password').strip()
        register_password_confirm = request.form.get('password_confirm').strip()
        print('+++++++++++++++++++++++++++')
        
        controller = WelcomeController(
            firstname=register_firstname,
            lastname=register_lastname,
            email=register_email,
            password=register_password,
            password_confirm=register_password_confirm
        )
        print(controller)
        reg_code = controller.valid_new_user()
        print("reg code is",reg_code)
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
            print(otp)
            if otp == 1:
                flash(ERROR_EMAIL_NOT_SENT, ERROR_MESSAGE_CATEGORY)
            else:
                session['otp'] = otp
                session['registration_complete'] = True
                session['register_details'] = {
                    "firstname": register_firstname,
                    "lastname": register_lastname,
                    "email": register_email,
                    "password": register_password
                }
                flash(f'Thank you, {register_firstname}! A 6-digit confirmation code has been sent to your email address ({register_email}).', 'success')
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
            user_id = controller.register()
            #session['user_id'] = user_id
            flash(f'Registration completed! Your email has been verified successfully, {register_details["firstname"]}!', 'success')
            #session['logged_in'] = True
            session['user_registered'] = True
            
            # Clear registration state
            session.pop('registration_complete', None)
            session.pop('otp', None)
            session.pop('register_details', None)

            return redirect(url_for('login'))
        else:
            flash(WARNING_INVALID_OTP, ERROR_MESSAGE_CATEGORY)
    
    
    if 'registration_complete' in session :
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
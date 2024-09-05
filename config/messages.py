"""This module defines messages to display accross the Flask application interfaces"""
# Success messages
SUCCESS_REGISTRATION = 'Your registration was successful!'
SUCCESS_LOGIN = 'Welcome back'
SUCCESS_LOGOUT = 'You have been logged out successfully.'
SUCCESS_CATEGORY_ADDED = 'Category added successfully!'
SUCCESS_CATEGORY_REMOVED = 'Category removed!'
SUCCESS_SENTIMENT_ADDED = 'Sentiment added successfully!'
SUCCESS_SENTIMENT_REMOVED = 'Sentiment removed!'

# Error messages
ERROR_INVALID_EMAIL = 'Invalid email address.'
ERROR_INCORRECT_CREDENTIALS = 'Incorrect email or password!'
ERROR_MISSING_FIELDS = 'Please fill in all the fields.'
ERROR_PASSWORD_MISMATCH = 'The two passwords do not match!'
ERROR_EMAIL_IN_USE = 'Email address already in use!'
ERROR_UNKNOWN = 'An unexpected error occurred. Please try again.'
ERROR_EMAIL_NOT_SENT = 'Email not sent! Are you sure your email address is correct?'
ERROR_WEAK_PASSWORD='At least 6 characters required for password!'


# Warning messages
WARNING_INVALID_OTP = 'Incorrect confirmation code. Please try again.'

import hashlib
import secrets
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import os


# Add the project root directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import SENDER_ADDRESS,PASSWORD
def encrypt_password(password):
    password = password.encode('utf-8')  # Convert the password to bytes
    encrypted_passwd = hashlib.sha256(password).hexdigest()
    return encrypted_passwd

def is_empty(text):
    return text==None or text==''

def generate_otp():
    # Generate a random 6-digit number
    code = secrets.randbelow(900000) + 100000
    return code

def send_email(receiver_addr,subject,body):
    try:
        connection=SMTP('smtp.gmail.com',587)
        connection.starttls()
        
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = SENDER_ADDRESS
        msg['To'] = receiver_addr
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        connection.login(user=SENDER_ADDRESS,password=PASSWORD)
        
        # Send the email
        connection.sendmail(SENDER_ADDRESS, receiver_addr, msg.as_string())
        sent=True
    except Exception as e:
        print(e)
        sent=False
    finally:
        # Close the connection
        connection.quit()

    return sent

#SMTPRecipientsRefused(senderrs)
if __name__=="__main__":
    x=send_email(receiver_addr='ezechieladede@gmail.com',subject='Test',body='This is just for test')
    print(x)

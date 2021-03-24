import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from hcss_blog import mail

def send_new_user_email(user):
    msg = Message('HCSS Blog - New User Registration',
                  sender='mpolatpy@gmail.com',
                  recipients=['mpolat@hampdencharter.org'])
    msg.body = f'''
This is an automated email notification from HCSS Blog.

A new user is submitted and awating for approval.
- user: {user.username}
- email: {user.email}

Please note that the post will only be available for public after a site admin approves the post.

Thank you
'''
    mail.send(msg)

def send_user_authorization_email(user):
    msg = Message('Registration Request Status',
                  sender='mpolatpy@gmail.com',
                  recipients=[user.email])
    msg.html = f'''
Hi {user.username.title()},
<br><br>
A decision has been made for your registration request. Your registration request is {user.status}.
<br>
You may visit the HCSS Blog using the
<a href= "{url_for('main.index', _external=True)}">link</a>.
<br><br>
If you have any questions, please contact HCSS Blog Team.
<br><br>
HCSS Blog Team
'''
    mail.send(msg)

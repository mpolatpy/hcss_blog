import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from hcss_blog import mail, S3_KEY, S3_SECRET, S3_BUCKET
from hcss_blog.models import User
import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename

sender = os.environ.get('EMAIL_USER2')

# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, file_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + file_ext
#     picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
#
#     # resize image before saving
#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)
#
#     return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=sender,
                  recipients=[user.email])
    msg.html = f'''Hi {user.username},
<br><br>
You have requested to reset your password for HCSS Blog. If you did not make this request
then simply ignore this email and no changes will be made.
<br><br>
To reset your password, visit the following link:<br>
<a href= "{url_for('users.reset_token', token=token, _external=True)}">Reset Password</a><br>
<br>
HCSS Blog Team
'''
    mail.send(msg)

def notify_registration(user):
    recipients = [user.email for user in User.query.filter(User.role=='admin').all()]
    msg = Message('New User Registration',
                  sender=sender,
                  recipients=recipients)
    msg.html = f'''Hi HCSS Blog Admin Team,
<br><br>
This is an automated email notification from HCSS Blog.<br>
A new user is registered for HCSS Blog. Please review the details below:<br>
Username: {user.username}<br>
Email: {user.email}
<br><br>
Please use the
<a href="{url_for('admin.authorize_user', user_id=user.id, _external=True)}">link</a>
to make a decision.
<br><br>
Thank you
'''
    mail.send(msg)

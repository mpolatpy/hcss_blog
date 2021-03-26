import os
# import secrets
# from PIL import Image
from flask import url_for, current_app
from hcss_blog import db
from hcss_blog.models import Post, User
from flask_mail import Message
from hcss_blog import mail
from datetime import datetime, timedelta
import calendar

# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, file_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + file_ext
#     picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)
#
#     # resize image before saving
#     output_size = (500, 500)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)
#
#     return picture_fn


def month_range(date_tag):
    first_day = datetime.strptime(date_tag, '%B %Y')
    num_days = calendar.monthrange(first_day.year, first_day.month)[1]
    last_day = first_day + timedelta(days=num_days)

    return first_day, last_day

def send_new_post_email(post):
    sender = os.environ.get('EMAIL_USER2')
    recipients = [user.email for user in User.query.filter(User.role=='admin').all()]
    msg = Message('HCSS Blog - New Post Notification',
                  sender=sender,
                  recipients=recipients)
    msg.body = f'''
This is an automated email notification from HCSS Blog. A new post is submitted and awating for approval.

- Author: {post.author.username}
- Title : {post.title}
- Date: {post.date_posted.strftime('%b %d, %Y')}

Please note that the post will only be available for public view after a site admin approves the post.

Thank you
'''
    mail.send(msg)

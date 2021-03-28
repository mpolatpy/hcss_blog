from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from hcss_blog.config import Config
import os
from flask_ckeditor import CKEditor

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('FLASK_BLOG_SECRET_KEY')
basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, 'site.db')
#heroku postgres
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER2')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS2')
mail = Mail(app)

app.config['CKEDITOR_PKG_TYPE'] = 'standard'
ckeditor = CKEditor(app)

S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
S3_KEY = os.environ.get("S3_ACCESS_KEY")
S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_LOCATION = "https://{}.s3.amazonaws.com/".format(S3_BUCKET)

from hcss_blog.users.routes import users
from hcss_blog.posts.routes import posts
from hcss_blog.main.routes import main
from hcss_blog.admin.routes import admin
from hcss_blog.errors.handlers import errors
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(admin)
app.register_blueprint(errors)

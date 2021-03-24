from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from hcss_blog.models import User, Post

class AuthorizeUserForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email Address',validators=[DataRequired(), Email()])
    account_role = SelectField('Account Role', choices=[('admin', 'Admin'), ('staff', 'Staff'), ('student','Student')], default='student')
    status = SelectField('Status', choices=[('approved','Approved'), ('pending','Pending'), ('rejected','Rejected')], default='pending')
    submit = SubmitField('Update User')

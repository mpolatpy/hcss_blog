from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    # content = TextAreaField('Content', validators=[DataRequired()])
    content = CKEditorField('Content')
    post_photo = FileField('Post Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    tags = StringField('Tags')
    submit = SubmitField('Submit Post')

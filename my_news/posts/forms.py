from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


class CreatePostForm(FlaskForm):
    cover = FileField('Cover', [FileRequired(), FileAllowed(('jpg', 'png'))])
    title = StringField('Title', [DataRequired()])
    body = TextAreaField('Body', [DataRequired()])
    submit = SubmitField('Post')


class CreateCommentForm(FlaskForm):
    body = TextAreaField('Body', [DataRequired()])
    submit = SubmitField('Comment')

from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired


class CreateNewsForm(FlaskForm):
    # TODO: To end multiple file filed uploading and selecting cover
    cover = FileField('Cover', [FileRequired(), FileAllowed(('jpg', 'png'))])
    images = MultipleFileField('Images')
    title = StringField('Title', [DataRequired()])
    body = TextAreaField('Body', [DataRequired()])
    submit = SubmitField('Post')


class CreateCommentForm(FlaskForm):
    body = TextAreaField('Body', [DataRequired()])
    submit = SubmitField('Comment')

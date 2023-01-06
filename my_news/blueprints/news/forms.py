from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize


class CreateNewsForm(FlaskForm):
    cover = FileField('Cover', [FileRequired(), FileAllowed(('jpg', 'png', 'jpeg'), FileSize(5*1_000_000))])
    images = MultipleFileField('Images', [FileAllowed(('jpg', 'png', 'jpeg'), FileSize(5*1_000_000))])
    title = StringField('Title', [DataRequired()])
    body = TextAreaField('Body', [DataRequired()])
    submit = SubmitField('Post')


class EditNewsForm(FlaskForm):
    cover = FileField('Cover', [FileAllowed(('jpg', 'png'))])
    images = MultipleFileField('Images')
    title = StringField('Title', [DataRequired()])
    body = TextAreaField('Body', [DataRequired()])
    submit = SubmitField('Edit')

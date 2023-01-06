from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize


class EditAccountForm(FlaskForm):
    image = FileField('Image', [FileAllowed(('jpg', 'png', 'jpeg'), FileSize(5*1_000_000))])
    first_name = StringField('First name')
    last_name = StringField('Last name')
    description = TextAreaField('Description')
    submit = SubmitField('Edit')
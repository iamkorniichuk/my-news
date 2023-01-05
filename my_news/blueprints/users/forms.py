from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed


class EditAccountForm(FlaskForm):
    image = FileField('Image', [FileAllowed(('jpg', 'png'))])
    first_name = StringField('First name')
    last_name = StringField('Last name')
    description = TextAreaField('Description')
    submit = SubmitField('Edit')
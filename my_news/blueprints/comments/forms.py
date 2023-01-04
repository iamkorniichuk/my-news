from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class CreateCommentForm(FlaskForm):
    body = TextAreaField('Body', [DataRequired()])
    submit = SubmitField('Comment')
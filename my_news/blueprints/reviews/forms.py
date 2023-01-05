from wtforms import SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class CreateReviewForm(FlaskForm):
    stars = RadioField('Stars', [DataRequired()], choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], coerce=int)
    body = TextAreaField('Body', [DataRequired()])
    submit = SubmitField('Post')

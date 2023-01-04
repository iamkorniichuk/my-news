from wtforms import SubmitField, TextAreaField, IntegerField, ValidationError
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class CreateReviewForm(FlaskForm):
    stars = IntegerField('Stars')
    body = TextAreaField('Body', [DataRequired()])
    submit = SubmitField('Post')


    def validate_stars(self, field):
        stars = field.data
        if 1 > stars or stars > 5:
            raise ValidationError('Stars need to be 1-5')

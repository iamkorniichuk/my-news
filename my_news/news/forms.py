from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class CreateNewsForm(FlaskForm):
    # TODO: To end multiple file filed uploading and selecting cover
    images = MultipleFileField('Images', [DataRequired()])
    title = StringField('Title', [DataRequired()])
    body = TextAreaField('Body', [DataRequired()])
    submit = SubmitField('Post')


class CreateCommentForm(FlaskForm):
    body = TextAreaField('Body', [DataRequired()])
    submit = SubmitField('Comment')

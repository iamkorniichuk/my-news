from wtforms import StringField, PasswordField, EmailField, SubmitField, ValidationError
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo
from my_news.models.users import users_model


class LoginForm(FlaskForm):
    login = StringField('Login', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Log In')

    def validate_login(self, field):
        if not users_model.exists(field.data):
            raise ValidationError('Such a user doesn\'t exist!')


class SignupForm(FlaskForm):
    email = EmailField('Email', [DataRequired()])
    login = StringField('Login', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    repeat_password = PasswordField('Repeat password', [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        if users_model.exists(email.data, column='email'):
            raise ValidationError('Email must be unique!')

    def validate_login(self, login):
        if users_model.exists(login.data):
            raise ValidationError('Login must be unique!')

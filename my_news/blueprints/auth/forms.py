from wtforms import StringField, PasswordField, EmailField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm
import my_news.db.models as models


class LoginForm(FlaskForm):
    login = StringField('Login', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Log In')


    def validate_login(self, field):
        if not models.users.exists(field.data):
            raise ValidationError('Such user doesn\'t exist!')

    
    def validate_password(self, field):
        if not models.users.auth(self.login.data, field.data):
            raise ValidationError('Invalid password!')


class SignupForm(FlaskForm):
    email = EmailField('Email', [DataRequired()])
    login = StringField('Login', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    repeat_password = PasswordField('Repeat password', [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_email(self, email):
        if models.users.exists(email.data, key='email'):
            raise ValidationError('Email must be unique!')


    def validate_login(self, login):
        if models.users.exists(login.data):
            raise ValidationError('Login must be unique!')

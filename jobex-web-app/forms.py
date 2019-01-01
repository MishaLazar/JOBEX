from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=12)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=12)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(min=6, max=12), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # @staticmethod
    # def validate_username(username):
    #     # todo should be validated by analyzing API response and not DB query
    #     user_validator = user.User.query.filter_by(username=username.data).first()
    #     if user_validator:
    #         raise ValidationError('This username is already taken, please choose another one..')
    #
    # @staticmethod
    # def validate_email(email):
    #     # todo should be validated by analyzing API response and not DB query
    #     email_validator = user.User.query.filter_by(username=email.data).first()
    #     if email_validator:
    #         raise ValidationError('This email is already taken, please choose another one..')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=12)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

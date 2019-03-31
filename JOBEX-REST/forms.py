from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=12)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=12)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(min=6, max=12), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=12)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=12)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AddPositionForm(FlaskForm):
    position_name = StringField('Position Name', validators=[DataRequired()])
    position_department = StringField('Position Department', validators=[DataRequired()])
    position_active = BooleanField('Position Active', validators=[DataRequired()])
    # todo complete the object
    submit = SubmitField('Add Position')

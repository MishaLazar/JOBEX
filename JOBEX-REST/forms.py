from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class Select2MultipleField(SelectMultipleField):

    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=12)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=12)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(min=6, max=12), EqualTo('password')])
    company_name = StringField('Company Name', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=12)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=12)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AddPositionForm(FlaskForm):
    position_name = StringField('Position Name', validators=[DataRequired()])
    position_department = StringField('Position Department', validators=[DataRequired()])
    position_active = BooleanField('Position Active')
    position_location = StringField('Position Location', validators=[DataRequired()], description=u"where is it based?")
    position_skills = Select2MultipleField(u"Position Skills", [], choices=[],
                                           description=u"Choose the position required skills",
                                           render_kw={"multiple": "multiple"})
    comment = StringField('Comment', description=u"anything to add?")
    submit = SubmitField('Add Position')

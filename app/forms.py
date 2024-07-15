from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class RegistrationForm(FlaskForm):
    """
    Form for users to create a new account.
    Fields:
        - username: Required string field for the username.
        - email: Required string field for the email, must be a valid email format.
        - password: Required password field for the password.
        - submit: Submit button for the form.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    """
    Form for users to log in to their account.
    Fields:
        - email: Required string field for the email, must be a valid email format.
        - password: Required password field for the password.
        - submit: Submit button for the form.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


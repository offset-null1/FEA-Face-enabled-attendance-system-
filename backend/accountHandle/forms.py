"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)

class SignupForm(FlaskForm):
    """ User sign-up form """
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired()
        ]
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a strong password.')
        ]
    )
    
    confirm = PasswordField(
        'Confirm your password.',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    
    
class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter the valid email.')
        ]
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]    
    )
    
    submit = SubmitField('Log In')
    
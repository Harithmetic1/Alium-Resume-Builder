from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, 
                BooleanField, SubmitField, TextAreaField)
from wtforms.validators import (DataRequired, ValidationError, 
                        Email, EqualTo, Length)
from app.models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', 
                    validators=[DataRequired(), Email()])
    firstname = StringField('Firstname', 
                    validators=[DataRequired()])
    lastname = StringField('Lastname', 
                    validators=[DataRequired()])
    password = PasswordField('Password', 
                    validators=[DataRequired()])
    confirm_password = PasswordField('Password', 
                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use')

class LoginForm(FlaskForm):
    email = StringField('Email', 
                    validators=[DataRequired()])
    password = PasswordField('Password', 
                    validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', 
                    validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Change')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Invalid email')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', 
                    validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
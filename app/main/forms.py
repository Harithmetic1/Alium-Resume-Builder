from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import (
    StringField, PasswordField, SelectField,
    SubmitField, BooleanField, TextAreaField)
from wtforms.validators import (
    DataRequired, Length, 
    Email, EqualTo, ValidationError)
from flask_wtf.file import FileField, FileAllowed
from app.models import User


class UpdateAccountForm(FlaskForm):
    firstname = StringField('Firstname', 
                            validators=[DataRequired(), 
                                        Length(min=2, max=20)])
    lastname = StringField('Lastname', 
                            validators=[DataRequired(), 
                                        Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(),
                                 Email()])
    phone = StringField('Phone Number', 
                        validators=[DataRequired()])
    state = StringField('website', 
                        validators=[DataRequired()])
    current_occupation = StringField('Job Title', 
                        validators=[DataRequired()])
    city = StringField('city', 
                        validators=[DataRequired()])
    state = StringField('state', 
                        validators=[DataRequired()])
    country = StringField('country', 
                        validators=[DataRequired()])
    about_me = TextAreaField('Professional Summary', 
                            validators=[DataRequired()])
    picture = FileField('Update Profile Picture', 
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Profile')


    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username taken. Please choose another.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email taken. Please choose another.')
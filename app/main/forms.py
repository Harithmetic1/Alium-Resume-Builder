from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_wtf.file import FileField, FileAllowed
from app.models import User


class UpdateAccountForm(FlaskForm):
    firstname = StringField('Firstname')
    lastname = StringField('Lastname')
    email = StringField('Email',
                        validators=[Email()])
    phone = StringField('Phone Number',)
    state = StringField('state')
    current_occupation = StringField('Job Title')
    city = StringField('city')
    state = StringField('state')
    country = StringField('country')
    about_me = TextAreaField('Professional Summary')
    picture = FileField('Update Profile Picture', 
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save and Next')
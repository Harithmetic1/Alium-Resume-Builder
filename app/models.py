from datetime import datetime
from flask_login import UserMixin
from flask import current_app as app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def get_user(id):
    return User.query.get_or_404(int(id))

#Association table for user and Experience models
users_works = db.Table('users_jobs',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('job_id', db.Integer, db.ForeignKey('experience.id'))
    )

#Association table for user and Languages models
users_languages = db.Table('users_languages',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('language_id', db.Integer, db.ForeignKey('languages.id'))
    )

#Association table for user and skills models
users_skills = db.Table('users_skills',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
    )

#Association table for user and Hobbies models
users_hobbies = db.Table('users_hobbies',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('hobbie_id', db.Integer, db.ForeignKey('hobbies.id'))
    )

#Association table for user and Education models
users_educations = db.Table('users_educations',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('education_id', db.Integer, db.ForeignKey('education.id'))
    )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    phone = db.Column(db.String)
    firstname = db.Column(db.String, index=True)
    lastname = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    about_me = db.Column(db.Text)
    current_template=db.Column(db.String)
    avatar=db.Column(db.String)
    city=db.Column(db.String)
    state=db.Column(db.String)
    country=db.Column(db.String)
    current_occupation=db.Column(db.String)
    current_job = db.Column(db.String)
    works=db.relationship('Experience', #connects the user to the experience model
                        secondary=users_works,
                        backref=db.backref('users', lazy='dynamic'),
                        lazy='dynamic')
    educations=db.relationship('Education', #connects the user to the interest model
                        secondary=users_educations,
                        backref=db.backref('users', lazy='dynamic'),
                        lazy='dynamic')
    skills=db.relationship('Skill', #connects the user to the skill model
                        secondary=users_skills,
                        backref=db.backref('users', lazy='dynamic'),
                        lazy='dynamic')
    hobbies=db.relationship('Hobbies', #connects the user to the hobby model
                        secondary=users_hobbies,
                        backref=db.backref('users', lazy='dynamic'),
                        lazy='dynamic')
    languages=db.relationship('Languages', #connects the user to the language model
                        secondary=users_languages,
                        backref=db.backref('users', lazy='dynamic'),
                        lazy='dynamic')

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f'<User {self.email}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_token(self, expires_sec=1800):
        '''Generates a timed token to reset password/confirm account'''
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod 
    def verify_reset_token(token):
        '''Verifies the timed token generated in the function above'''
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String, index=True, nullable=False)
    company = db.Column(db.String, index=True, nullable=False)
    date_started = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_end = db.Column(db.DateTime)
    description = db.Column(db.Text)

    def __repr__(self):
        '''This functions describes how the experience model will be displayed'''
        return f"Experience('{self.title}', '{self.date_started}')"
    
    def get_json(self):
        data = {
            'Job Position': self.title,
            'Company Name': self.company,
            'date started': self.date_started,
            'description': self.description
        }
        data['date end'] = self.date_end if self.date_end else 'Present'
        return data

    def create_data(self, data):
        for field in ['title', 'company', 'date started', 'date end', 'description']:
            if field in data:
                setattr(self, field, data[field])


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    course = db.Column(db.String, index=True, nullable=False)
    school = db.Column(db.String, index=True, nullable=False)
    date_started = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_end = db.Column(db.DateTime)
    location=db.Column(db.String)
    degree_name = db.Column(db.String)

    def __repr__(self):
        '''This functions describes how the education model will be displayed'''
        return f"Education('{self.course}', '{self.date_started}')"
    
    def create_data(self, data):
        for field in ['course', 'school', 'date started', 'date end', 'degree name']:
            if field in data:
                setattr(self, field, data[field])
    
    def get_json(self):
        data = {
            'Course': self.course,
            'School': self.school,
            'date started': self.date_started,
            'degree name': self.degree_name
        }
        data['date end'] = self.date_end if self.date_end else 'Present'
        return data

class Hobbies(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, index=True, unique=True)

    def __repr__(self):
        '''This functions describes how the hobby model will be displayed'''
        return f"Hobbies('{self.name}')"
    
    def create_data(self, data):
        for field in ['name']:
            if field in data:
                setattr(self, field, data[field])
    
    def get_json(self):
        return {
            'name': self.name
        }

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, index=True, unique=True)
    level = db.Column(db.Integer)

    def create_data(self, data):
        for field in ['name', 'level']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        '''This functions describes how the skill model will be displayed'''
        return f"Skill('{self.name}')"
    
    def get_json(self):
        return {
            'name': self.name,
            'level': self.level
        }

class Languages(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, index=True, unique=True)
    level = db.Column(db.Integer)

    def create_data(self, data):
        for field in ['name', 'level']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        '''This functions describes how the language model will be displayed'''
        return f"Language('{self.name}')"

    def get_json(self):
        return {
            'name': self.name,
            'level': self.level
        }



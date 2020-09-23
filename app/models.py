from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def get_user(id):
    return User.query.get_or_404(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    phone = db.Column(db.String)
    firstname = db.Column(db.String, index=True)
    lastname = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    about_me = db.Column(db.Text)
    current_job = db.Column(db.String)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String, index=True, nullable=False)
    company = db.Column(db.String, index=True, nullable=False)
    date_started = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_end = db.Column(db.String, index=True, nullable=False)
    description = db.Column(db.Text)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    course = db.Column(db.String, index=True, nullable=False)
    school = db.Column(db.String, index=True, nullable=False)
    date_started = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_end = db.Column(db.DateTime)
    degree_name = db.Column(db.String)

class Hobbies(db.Model):
    id = db.Column(db.String, primary_key=True, index=True)
    name = db.Column(db.String, index=True, unique=True)

class Skills(db.Model):
    id = db.Column(db.String, primary_key=True, index=True)
    name = db.Column(db.String, index=True, unique=True)

class Languages(db.Model):
    id = db.Column(db.String, primary_key=True, index=True)
    name = db.Column(db.String, index=True, unique=True)


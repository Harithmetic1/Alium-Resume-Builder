from flask import (render_template, url_for, request,
    redirect, flash, current_app as app)
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from app import db
from app.auth import auth
from app.main import main
from app.models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('app.main.index'))
    if request.method == 'POST':
        u = User.query.filter_by(email=request.form['email']).first()
        if u and u.check_password(request.form['password']):
            login_user(u)
            return redirect(url_for('app.main.index'))
        flash('Invalid email or password')
    return render_template('SignIn.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup(): 
    if current_user.is_authenticated:
        return redirect(url_for('app.main.index'))
    if request.method == 'POST':
        u = User.query.filter_by(email=request.form['email']).first()
        if not u:
            u = User(email=request.form['email'],
                    firstname=request.form['fullname'].split(' ')[0],
                    lastname=request.form['fullname'].split(' ')[1]
                )
            u.set_password(request.form['password'])
            db.session.add(u)
            db.session.commit()
            flash('Account created  successfully')
            login_user(u)
            return redirect(url_for('app.main.index'))
        flash('Email chosen')
    return render_template('Signup.html')

@auth.route('/login/linkeidn')
def login_linkedin():
    return {'message': 'In progress'}

@auth.route('/login/google')
def login_google():
    return {'message': 'In progress'}

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('app.main.index'))
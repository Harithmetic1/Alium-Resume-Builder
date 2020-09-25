from flask import (render_template, url_for, request,
    redirect, flash, current_app as app)
from app import mail
from flask_mail import Message
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from app import db
from app.auth import auth
from app.auth.forms import (LoginForm, RegistrationForm, 
                ResetPasswordRequestForm, ResetPasswordForm)
from app.main import main
from app.models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('app.main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        f=open('file.txt', 'w')
        print(f'{form.password.data}, {form.email.data}', file=f)
        f.close()
        if u and u.check_password(form.password.data):
            login_user(u)
            return redirect(url_for('app.main.index'))
        flash('Invalid email or password')
    return render_template('SignIn.html', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup(): 
    if current_user.is_authenticated:
        return redirect(url_for('app.main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if not u:
            if len(form.fullname.data.split(' ')) < 2:
                f = open('file.txt', 'w')
                print(form.fullname.data.split(' '), file=f)
                f.close()
            else:
                u = User(email=form.email.data,
                        firstname=form.fullname.data.split(' ')[0],
                        lastname=form.email.data.split(' ')[1]
                    )
                u.set_password(form.password.data)
                db.session.add(u)
                db.session.commit()
                flash('Account created  successfully')
                login_user(u)
                return redirect(url_for('app.main.index'))
        flash('Email chosen')
    return render_template('Signup.html', form=form)

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


def send_email(sender, recipient, subject, body, **kwargs):
    msg = Message(subject=subject, 
                sender=sender,
                body=body,
                recipients=[recipient.email])
    msg.html = html if html else None
    mail.send(msg)


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('app.main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token=user.get_reset_token()
        body=render_template('reset-password-mail.txt',
                            token=token, 
                            website=url_for('app.main.index'))
        html=render_template('reset-password-mail.html',
                            token=token, 
                            website=url_for('app.main.index'))
        send_reset_email(app.config['MAIL_USERNAME'],
                        user, 
                        'Reset Password Request - [Alium || Resume Builder]',
                        body, html=html,
                        token=token)
        flash('An email has been sent to you with instructions to resetting your password', 'info')
    return render_template('reset_request.html', 
                            title='Reset Password',
                            form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Token is invalid or has expired', 'warning')
        return redirect(url_for('app.main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data)
        user.password=hashed_password
        db.session.commit()
        flash(f'Password has been updated! You can now login', 'success')
        return redirect(url_for('app.auth.login'))
    return render_template('reset_token.html', 
                            title='Reset Password',
                            form=form)


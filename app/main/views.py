from flask import (render_template, url_for, abort, make_response, request, jsonify,
    redirect, flash, current_app as app)
from flask_login import login_required, current_user
import pdfkit
from app import db
from app.main import main
from app.auth import auth
from app.main.utils import save_pic
from app.main.forms import UpdateAccountForm
from app.models import User, Education, Experience, Hobbies, Skill, Languages
from app.emails import send_email

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/help')
def help():
    return render_template('steps.html')

@main.route('/pdf-resume')
@login_required
def generate_pdf():
    import os
    if not current_user.current_template:
        return {
            'error': 'Invalid request', 
            'message': 'You did not choose any template yet'
        }
    template = f'user-{current_user.current_template}-pdf.html'
    hobbies = current_user.hobbies.all()
    if len(hobbies) > 2:
        hbs = [hobbies[i: i+2] for i in range(len(hobbies)-2)]
    else:
        hbs = [hobbies]
    pdf = render_template(template, hobbies=hbs, len=len)
    css = [
        os.path.join(app.root_path, 'static/css/bootstrap.min.css'),
        os.path.join(app.root_path, 'static/css/styles.css'),
        os.path.join(app.root_path, 'static/assets/navbar.css'),
        os.path.join(app.root_path, 'static/assets/gemheart.css'),
        os.path.join(app.root_path, 'static/js/jquery-2.1.4.min.js'),
        os.path.join(app.root_path, 'static/js/bootstrap.min.js'),
        os.path.join(app.root_path, 'static/assets/app.js'),
        os.path.join(app.root_path, 'static/assets/images/Ellipse 8.png')
        # "https://kit.fontawesome.com/dc7f1f050e.js"
    ]
    js = [
        
    ]
    options = {'enable-local-file-access': True}
    pdf=pdfkit.from_string(pdf, output_path=current_user.avatar.split('.')[0]+'.pdf',  
                configuration=app.config['PDF_TO_HTML'], css=css, options=options)
    response = make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='inline; filename.pdf'

    return response

@main.route('/templates')
def templates():
    return render_template('templates.html')

@main.route('/template')
@login_required
def resume_template():
    try:
        template = request.args.get('template')
        if template and template == 'gemheart':
            current_user.current_template = template
            db.session.commit()
        else:
            flash('Your preferred template does not currently exist, Our developers are currently working on making it live')
            return redirect(url_for('app.main.templates'))
    except Exception as e:
        return abort(500)
    else:
        return redirect(url_for('app.main.add_profile'))

@main.route('/add-profile', methods=['GET', 'POST'])
@login_required
def add_profile():
    if not current_user.current_template or current_user.current_template != 'gemheart':
        flash('Invalid template')
        return redirect(url_for('app.main.templates'))
    form = UpdateAccountForm()
    if form.is_submitted():
        if form.email.data != current_user.email:
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash('Invalid email, email has been chosen by another user')
                return redirect(url_for('app.main.add_profile'))
            else:
                current_user.email = form.email.data
        else:
            current_user.email = form.email.data
        if form.picture.data:
            current_user.avatar = save_pic(form.picture.data)
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.phone = form.phone.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.country = form.country.data
        current_user.current_occupation = form.current_occupation.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        return redirect(url_for('app.main.add_experience'))
    elif request.method == 'GET':
        form.firstname.data=current_user.firstname
        form.lastname.data=current_user.lastname
        form.email.data=current_user.email
        form.phone.data=current_user.phone
        form.city.data=current_user.city
        form.state.data=current_user.state
        form.country.data=current_user.country
        form.current_occupation.data=current_user.current_occupation
        form.about_me.data=current_user.about_me
    return render_template('personal-info.html', form=form)


@main.route('/add-experience', methods=['POST', 'GET'])
def add_experience():
    return render_template('work-experience.html')

@main.route('/add-education', methods=['POST', 'GET'])
def add_education():
    return render_template('education.html')

@main.route('/add-skill', methods=['POST', 'GET'])
def add_skill():
    return render_template('skills.html')

@main.route('/add-hobby', methods=['POST', 'GET'])
def add_hobby():
    return render_template('hobbies.html')

@main.route('/preview')
@login_required
def preview():
    if current_user.current_template:
        template = f'user-{current_user.current_template}.html'
    else:
        template = None
    if template != 'user-gemheart.html':
        flash('Your preferred template does not currently exist, Our developers are currently working on making it live')
        return redirect(url_for('app.main.templates'))
    hobbies = current_user.hobbies.all()
    if len(hobbies) > 2:
        hbs = [hobbies[i: i+2] for i in range(len(hobbies)-2)]
    else:
        hbs = [hobbies]
    return render_template(template, hobbies = hbs, len=len)

def send_resume_as_mail(user):
    template = f'user-{user.current_template}-pdf.html'
    pdf = redirect(url_for('app.main.generate_pdf'))
    body=render_template('mail/resume-mail.txt',
                            user=user,
                            website=url_for('app.main.index'))
    html=render_template('mail/resume-mail.html',
                            user=user,
                            website=url_for('app.main.index'))
    pdf=pdfkit.from_string(pdf, False, 
                configuration=app.config['PDF_TO_HTML'])
    response = make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='inline; filename.pdf'
    sent = send_email(sender=app.config['MAIL_USERNAME'],
            subject='Your Resume | Alium-Resume',
            recipient=user.email,
            body=body,
            attachment=response)
    return sent if sent else None

@main.route('/resume/email')
@login_required
def send_resume_mail():
    sent = send_resume_as_mail(current_user)
    flash('Email sent successfully') if sent else None
    return  redirect(url_for('app.main.index'))
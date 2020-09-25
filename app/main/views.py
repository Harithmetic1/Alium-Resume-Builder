from flask import (render_template, url_for, abort, make_response, request,
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
    if not current_user.current_template:
        return {
            'error': 'Invalid request', 
            'message': 'You did not choose any template yet'
        }
    template = f'user-{current_user.current_template}.html'
    pdf = render_template(template)
    pdf=pdfkit.from_string(pdf, False, 
                configuration=app.config['PDF_TO_HTML'])
    response = make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='inline; filename.pdf'

    return response

@main.route('/template')
@login_required
def resume_template():
    try:
        template = request.args.get('template')
        if template:
            current_user.current_template = template if template else None
            db.session.commit()
        else:
            return abort(403)
    except Exception as e:
        return {'error': 'Something went wrong', 'message': str(e)}
    else:
        return redirect(url_for('app.main.add_profile'))

@main.route('/add-profile', methods=['GET', 'POST'])
@login_required
def add_profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # validate and add profile to db
        current_user.avatar = save_pic(form.picture.data) if not current_user.avatar \
            else save_pic(form.picture.data, current_user.avatar)
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.country = form.country.data
        current_user.current_occupation = form.current_occupation.data
        current_user.about_me = form.about_me.data
        db.session.commit()
    
        return redirect(url_for('app.main.index'))
    current_user.avatar = save_pic(form.picture.data) if not current_user.avatar \
            else save_pic(form.picture.data, current_user.avatar)
    form.firstname.data=current_user.firstname
    form.lastname.data=current_user.lastname
    form.email.data=current_user.email
    form.phone.data=current_user.phone
    form.city.data=current_user.city
    form.state.data=current_user.state
    form.country.data=current_user.country
    form.current_occupation.data=current_user.current_occupation
    form.about_me.data=current_user.about_me
    return render_template('profile.html')

@main.route('/preview')
@login_required
def preview():
    if current_user.current_template == 'adolfa':
        template = 'user-adolfa.html'
    elif current_user.current_template == 'gemheart':
        template = 'user-gemheart.html'
    elif current_user.current_template == 'pixel':
        template = 'user-pixel.html'
    elif current_user.current_template == 'empire':
        template = 'user-empire.html'
    else:
        return {
            'error': 'Server Error',
            'message': 'Template does not currently exist, Our developers are working on making the template live' 
        }
    return render_template(template)

def send_resume_as_mail(user):
    template = f'user-{user.current_template}.html'
    pdf = render_template(template)
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
    return sent if sent else redirect(url_for('app.main.index'))

@main.route('/resume')
@login_required
def resume():
    return {'message': 'In progress'}

@main.route('/templates')
def templates():
    return render_template('templates.html')
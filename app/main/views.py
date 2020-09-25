from flask import (render_template, url_for, abort, make_response, request,
    redirect, flash, current_app as app)
from flask_login import login_required, current_user
import pdfkit
from app import db
from app.main import main
from app.auth import auth
from app.main.utils import save_pic
from app.models import User, Education, Experience, Hobbies, Skill, Languages

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
    if request.method == 'POST':
        # validate and add profile to db
        # current_user.avatar = save_pic(form.picture.data) if not current_user.avatar \
        #      else save_pic(form.picture.data, current_user.avatar)
    
        return redirect(url_for('app.main.index'))
        
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

@main.route('/resume')
@login_required
def resume():
    if not current_user.is_authenticated: 
        return redirect(url_for('app.auth.login'))
    return {'message': 'In progress'}

@main.route('/templates')
def templates():
    return render_template('templates.html')
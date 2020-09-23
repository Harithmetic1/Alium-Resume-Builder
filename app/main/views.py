from flask import (render_template, url_for, abort, make_response,
    redirect, flash, current_app as app)
import pdfkit
from app.main import main
from app.auth import auth
from app.models import User

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/help')
def help():
    return render_template('steps.html')

@main.route('/template/<template>')
def resume_template(template):
    if template == 'gemheart':
        pdf = render_template('user-gemheart.html')
    elif template == 'empire':
        pdf = render_template('user-empire.html')
    elif template == 'adolfa':
        pdf = render_template('user-adolfa.html')
    elif template == 'pixel':
        pdf = render_template('user-pixel.html')
    else:
        return abort(404)
    pdf=pdfkit.from_string(pdf, False, 
                configuration=app.config['PDF_TO_HTML'])
    response = make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='inline; filename.pdf'

    return response

@main.route('/resume')
def resume():
    return {'message': 'In progress'}

@main.route('/templates')
def templates():
    return render_template('templates.html')
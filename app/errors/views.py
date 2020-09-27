from flask import render_template, redirect, url_for
from app.errors import errors

@errors.app_errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500

@errors.app_errorhandler(400)
def client_error(e):
    return render_template('errors/400.html'), 400
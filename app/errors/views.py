from flask import render_template, redirect, url_for
from app.errors import errors

@errors.errorhandler(404)
def not_found(e):
    return {
        'error': 'Not Found',
        'message': 'The page you requested for isn\'t available on this server'
    }, 404

@errors.errorhandler(500)
def server_error(e):
    return {
        'error': 'Server Error',
        'message': 'We\'re sorry. Our developers have been contacted and they\'re working on it'
    }, 500

@errors.errorhandler(400)
def client_error(e):
    return {
        'error': 'Not accepted',
        'message': 'The request you sent can\'t be processed'
    }, 400
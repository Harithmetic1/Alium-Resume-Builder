from flask import render_template
from app.errors import errors

@errors.errorhandler(404)
def not_found(e):
    return {
        'error': 'Not found'
    }, 404

@errors.errorhandler(500)
def server_error(e):
    return {
        'error': 'Not found'
    }, 500

@errors.errorhandler(400)
def client_error(e):
    return {
        'error': 'Not found'
    }, 400
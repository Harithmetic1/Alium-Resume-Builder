from flask import Blueprint

errors = Blueprint(__name__, 'errors')

from app.errors import views
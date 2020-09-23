from flask import Blueprint

auth = Blueprint(__name__, 'auth')

from app.auth import views
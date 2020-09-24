from flask import Blueprint

main = Blueprint(__name__, 'main')
from app.main import views
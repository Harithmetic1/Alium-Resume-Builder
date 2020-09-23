from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
login_manager.login_view = 'app.auth.login'
login_manager.login_message = 'Please login to view this page'

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app import models

    from app.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from app.errors import errors
    app.register_blueprint(errors, url_prefix='/errors')

    from app.main import main
    app.register_blueprint(main, url_prefix='/dashboard')

    return app
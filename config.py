import os, pdfkit
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY=os.environ.get('SECRET_KEY')
    # PDF_TO_HTML=pdfkit.configuration(wkhtmltopdf = os.environ.get('PDF_TO_HTML'))
    SQLALCHEMY_TRACK_MODIFICATIONS=1
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    MAIL_SERVER=os.environ.get('MAIL_SERVER')
    MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS')


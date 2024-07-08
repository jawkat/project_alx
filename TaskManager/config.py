""" all configuration parameters """
import os


class Config:
    """ Configuration class """
    # Set the secret key
    SECRET_KEY = os.urandom(30)

    # Set up the sqlite database path and URI
    DB_NAME = "First_base"
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, DB_NAME + '.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'


    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = 'noreply@demo.com'

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')



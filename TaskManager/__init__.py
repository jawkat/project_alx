""" init file """
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# Set the secret key
app.config['SECRET_KEY'] = os.urandom(30)

# Set up the sqlite database path and URI
DB_NAME = "First_base"
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, DB_NAME + '.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'


# Set up the mysql database path and URI
# app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://sqluser:password@localhost/taskflow_db'

# Initialize the database
db = SQLAlchemy(app)

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = "Please log in to access this page. Thanks"


def create_database():
    """ create database if not exists"""
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            print("created")




# Import routes after app and db initialization to avoid circular imports
from TaskManager import routes

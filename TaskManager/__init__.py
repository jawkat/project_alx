""" init file """
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from TaskManager.config import Config





# Set up the mysql database path and URI
# app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://sqluser:password@localhost/taskflow_db'

# Initialize the database
db = SQLAlchemy()

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'



mail = Mail()

login_manager.login_message = "Please log in to access this page. Thanks"


def create_database():
    """ create database if not exists"""
    if not os.path.exists(Config.db_path):
        with app.app_context():
            db.create_all()
            print("created")






def create_app(config_class=Config):
    """ creates an instance of the give config class """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Import routes after app and db initialization to avoid circular imports
    from TaskManager.users.routes import users
    from TaskManager.tasks.routes import tasks
    from TaskManager.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(tasks)
    app.register_blueprint(main)

    return app


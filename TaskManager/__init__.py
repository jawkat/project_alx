from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

# app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://sqluser:password@localhost/taskflow_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///first_base.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = "Please log in to access this page. Thanks"

from TaskManager import routes

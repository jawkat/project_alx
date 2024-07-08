from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)

# Models definition here...

@app.route('/')
def index():
    with app.app_context():
        db.create_all()
        db.session.commit()
    return 'Database tables created successfully!'

if __name__ == '__main__':
    app.run(debug=True)

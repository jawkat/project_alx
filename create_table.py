from TaskManager import app, db
from TaskManager.models import User,TaskCollaborator,Task,Note

# Create an application context
with app.app_context():
    # Create all tables
    db.create_all()
    db.session.commit()

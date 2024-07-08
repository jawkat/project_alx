from datetime import datetime, timedelta
import random
from lorem_text import lorem  # You can use this library to generate paragraphs

from TaskManager import app, db, create_database
from TaskManager.models import User, Task, Note

# Sample user IDs (you should replace these with actual user IDs from your User table)
user_ids = [1, 2]

# Sample titles
titles = [
    "Task One", "Task Two", "Task Three", "Task Four", "Task Five",
    "Task Six", "Task Seven", "Task Eight", "Task Nine", "Task Ten"
]

# Sample statuses and priorities
statuses = ['in progress', 'completed', 'pending']
priorities = ['low', 'medium', 'high']

# Create the database if it doesn't exist
create_database()

# Create an application context
with app.app_context():
    # Generate dummy data
    for i in range(10):
        description = lorem.paragraph()  # Generate a paragraph for task description
        task = Task(
            user_id=random.choice(user_ids),
            title=titles[i],
            description=description,
            status=random.choice(statuses),
            priority=random.choice(priorities),
            due_date=datetime.utcnow() + timedelta(days=random.randint(1, 30)),
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            updated_at=datetime.utcnow()
        )
        db.session.add(task)
        db.session.commit()  # Commit to get task.id for notes

        # Add notes for each task
        notes = []
        for j in range(10):
            note_content = lorem.paragraph()  # Generate a paragraph for note content
            note = Note(
                task_id=task.id,
                content=note_content,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                updated_at=datetime.utcnow()
            )
            notes.append(note)
        db.session.add_all(notes)
        db.session.commit()

print("Dummy data for tasks and notes inserted successfully.")

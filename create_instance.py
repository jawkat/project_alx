from TaskManager import app, db
from TaskManager.models import User, Post


#
user_1=User(username='jawad5', email='j5@k.com', password='pass')

# Create an application context
with app.app_context():
    db.session.add(user_1)
    db.session.commit()

# with app.app_context():
#     user = User.query.filter_by(username='JAWAD.K').first()
#     db.session.commit()
#     if user:
#         print(user)



post_1 = Post(title='blog 1', content= 'first post content', user_id = 1)

with app.app_context():
    db.session.add(post_1)
    db.session.commit()

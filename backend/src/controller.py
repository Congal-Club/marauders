from .database import db
from .models import User

def create_user(data):
  user = User(**data)

  db.session.add(user)
  db.session.commit()

  return user

def get_all_users():
  return db.session.query(User).all()

def get_user(user_id):
  return db.session.get(User, user_id)

def update_user(user_id, data):
  user = db.session.get(User, user_id)

  if not user:
    return None

  for key, value in data.items():
    setattr(user, key, value)

  db.session.commit()

  return user

def delete_user(user_id):
  user = db.session.get(User, user_id)

  if not user:
    return None

  db.session.delete(user)
  db.session.commit()

  return user

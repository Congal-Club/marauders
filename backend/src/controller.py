from .database import db
from .models import User, Post, Comment, Follow

class UserController:
  @staticmethod
  def create_user(data):
    user = User(**data)

    db.session.add(user)
    db.session.commit()
    
    return user

  @staticmethod
  def get_all_users():
    return db.session.query(User).all()

  @staticmethod
  def get_user(user_id):
    return db.session.get(User, user_id)

  @staticmethod
  def update_user(user_id, data):
    user = db.session.get(User, user_id)
    
    if not user:
      return None
    
    for key, value in data.items():
      setattr(user, key, value)
    
    db.session.commit()
    
    return user

  @staticmethod
  def delete_user(user_id):
    user = db.session.get(User, user_id)
    
    if not user:
      return None
    
    db.session.delete(user)
    db.session.commit()
    
    return user

class PostController:
  @staticmethod
  def create_post(data):
    pass

  @staticmethod
  def get_all_posts():
    pass

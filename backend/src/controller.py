import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from .database import db
from .models import User, Post, Comment, Follow

SECRET_KEY = "my_secret_key"

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

class AuthController:
  @staticmethod
  def signup(data):
    if db.session.query(User).filter_by(email=data.get("email")).first():
      return None, "User already exists"
    
    hashed_password = generate_password_hash(data["password"], method='pbkdf2:sha256')
    
    user = User(
      name=data["name"],
      lastName=data["lastName"],
      email=data["email"],
      password=hashed_password,
      image=data.get("image")
    )

    db.session.add(user)
    db.session.commit()
    
    return user, None

  @staticmethod
  def signin(data):
    user = db.session.query(User).filter_by(email=data.get("email")).first()
    
    if not user or not check_password_hash(user.password, data["password"]):
      return None, "Invalid email or password"

    token = jwt.encode(
      {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
      },
      SECRET_KEY,
      algorithm="HS256"
    )

    return {"token": token}, None

  @staticmethod
  def change_password(user_id, data):
    user = db.session.get(User, user_id)
    
    if not user or not check_password_hash(user.password, data.get("old_password")):
      return None, "Invalid user or password"

    new_hashed_password = generate_password_hash(data.get("new_password"), method='pbkdf2:sha256')
    user.password = new_hashed_password
    
    db.session.commit()
    
    return user, None

class PostController:
  @staticmethod
  def create_post(data):
    pass

  @staticmethod
  def get_all_posts():
    pass

import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from .database import db
from .models import User, Post, Comment, Follow, Like, Image

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
  def signout(user_authenticated):
    pass

  @staticmethod
  def change_password(user_authenticated, data):
    user = db.session.get(User, user_authenticated)
    
    if not user or not check_password_hash(user.password, data.get("old_password")):
      return None, "Invalid user or password"

    new_hashed_password = generate_password_hash(data.get("new_password"), method='pbkdf2:sha256')
    user.password = new_hashed_password
    
    db.session.commit()
    
    return user, None

class PostController:
  @staticmethod
  def create_post(user_id, data):
    post = Post(**data)
    post.user_id = user_id

    db.session.add(post)
    db.session.commit()
    
    return post

  @staticmethod
  def get_all_posts(user_id):
    return db.session.query(Post).all()

  @staticmethod
  def get_post(user_id, post_id):
    return db.session.get(Post, post_id)

  @staticmethod
  def update_post(user_id, post_id, data):
    post = db.session.get(Post, post_id)
    
    if not post:
      return None
    
    for key, value in data.items():
      setattr(post, key, value)
    
    db.session.commit()
    
    return post

  @staticmethod
  def delete_post(user_id, post_id):
    post = db.session.get(Post, post_id)
    
    if not post:
      return None
    
    db.session.delete(post)
    db.session.commit()
    
    return post

class CommentController:
  @staticmethod
  def create_comment(user_id, post_id, data):
    comment = Comment(**data)
    comment.user_id = user_id
    comment.post_id = post_id

    db.session.add(comment)
    db.session.commit()
    
    return comment

  @staticmethod
  def get_all_comments(user_id, post_id):
    return db.session.query(Comment).filter_by(post_id=post_id).all()

  @staticmethod
  def update_comment(user_id, post_id, comment_id, data):
    comment = db.session.get(Comment, comment_id)
    
    if not comment:
      return None
    
    for key, value in data.items():
      setattr(comment, key, value)
    
    db.session.commit()
    
    return comment

  @staticmethod
  def delete_comment(user_id, post_id, comment_id):
    comment = db.session.get(Comment, comment_id)
    
    if not comment:
      return None
    
    db.session.delete(comment)
    db.session.commit()
    
    return comment

class FollowController:
  @staticmethod
  def follow_user(auth_user, user_id):
    follow = Follow(user_following=auth_user, user_followed=user_id)

    db.session.add(follow)
    db.session.commit()

    return follow

  @staticmethod
  def unfollow_user(auth_user, user_id):
    follow = db.session.query(Follow).filter_by(user_following=auth_user, user_followed=user_id).first()

    if not follow:
      return None

    db.session.delete(follow)
    db.session.commit()

    return follow

  @staticmethod
  def get_all_followers(user_id):
    followers = db.session.query(Follow).filter_by(user_followed=user_id).all()
    return followers

  @staticmethod
  def get_all_following(user_id):
    following = db.session.query(Follow).filter_by(user_following=user_id).all()
    return following

class LikeController:
  @staticmethod
  def like_post(user_id, post_id):
    pass

  @staticmethod
  def unlike_post(user_id, post_id):
    pass

  @staticmethod
  def get_all_likes(user_id):
    pass

class ImageController:
  @staticmethod
  def upload_image(user_id, post_id, data):
    pass

  @staticmethod
  def get_all_images(user_id, post_id):
    pass

  @staticmethod
  def delete_image(user_id, post_id, image_id):
    pass

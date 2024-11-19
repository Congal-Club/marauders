from flask import Blueprint, jsonify, request
import re

from .controller import AuthController, UserController, PostController, CommentController, FollowController, LikeController, ImageController
from .middlewares import require_auth

class UserRoutes:
  def __init__(self):
    self.blueprint = Blueprint('users', __name__)
    self.blueprint.add_url_rule('/users', 'create', self.create, methods=['POST'])
    self.blueprint.add_url_rule('/users', 'all', self.all, methods=['GET'])
    self.blueprint.add_url_rule('/users/<int:user_id>', 'retrieve', self.retrieve, methods=['GET'])
    self.blueprint.add_url_rule('/users/<int:user_id>', 'update', self.update, methods=['PUT'])
    self.blueprint.add_url_rule('/users/<int:user_id>', 'delete', self.delete, methods=['DELETE'])

  def create(self):
    data = request.json
    
    required_fields = ["email", "password", "name"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
      return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    email = data["email"].strip()
    password = data["password"].strip()

    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_regex, email):
      return jsonify({"error": "Invalid email format"}), 400

    if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
      return jsonify({"error": "Password must be at least 8 characters long, including letters and numbers"}), 400

    user = UserController.create_user(data)

    if not user:
      return jsonify({"error": "Failed to create user"}), 400
    
    return jsonify(user.to_dict()), 201

  def all(self):
    users = UserController.get_all_users()
    return jsonify([user.to_dict() for user in users]), 200

  def retrieve(self, user_id):
    user = UserController.get_user(user_id)
    
    if user:
      return jsonify(user.to_dict()), 200
    
    return jsonify({"error": "User not found"}), 404

  def update(self, user_id):
    data = request.json

    if "email" in data:
      email = data["email"].strip()
      email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
      
      if not re.match(email_regex, email):
        return jsonify({"error": "Invalid email format"}), 400
        
    user = UserController.update_user(user_id, data)
    
    if user:
      return jsonify(user.to_dict()), 200
    
    return jsonify({"error": "User not found"}), 404

  def delete(self, user_id):
    user = UserController.delete_user(user_id)
    
    if user:
      return jsonify({"message": "User deleted"}), 200
    
    return jsonify({"error": "User not found"}), 404

class AuthRoutes:
  def __init__(self):
    self.blueprint = Blueprint('auth', __name__)
    self.blueprint.add_url_rule('/auth/sign-up', 'signup', self.signup, methods=['POST'])
    self.blueprint.add_url_rule('/auth/sign-in', 'signin', self.signin, methods=['POST'])
    self.blueprint.add_url_rule('/auth/sign-out', 'signout', self.signout, methods=['POST'])
    self.blueprint.add_url_rule('/auth/change-password', 'change_password', self.change_password, methods=['PUT'])

  def signup(self):
    data = request.json

    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
      return jsonify({"error": "Email and password are required"}), 400

    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(email_regex, email):
      return jsonify({"error": "Invalid email format"}), 400

    if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
      return jsonify({"error": "Password must be at least 8 characters long, including letters and numbers"}), 400

    user, error = AuthController.signup(data)
    
    if error:
      return jsonify({"error": error}), 400
    
    return jsonify(user.to_dict()), 201

  def signin(self):
    data = request.json

    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
      return jsonify({"error": "Email and password are required"}), 400

    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(email_regex, email):
      return jsonify({"error": "Invalid email format"}), 400

    token_data, error = AuthController.signin(data)
    
    if error:
      return jsonify({"error": error}), 401
    
    return jsonify(token_data), 200
  
  def signout(self):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    AuthController.signout(user_authenticated)
    
    return jsonify({"message": "Signed out successfully"}), 200

  def change_password(self):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    user, error = AuthController.change_password(user_authenticated, data)
    
    if error:
      return jsonify({"error": error}), 400
    
    return jsonify({"message": "Password updated successfully"}), 200

class PostRoutes:
  def __init__(self):
    self.blueprint = Blueprint('posts', __name__)
    self.blueprint.add_url_rule('/posts', 'create', self.create, methods=['POST'])
    self.blueprint.add_url_rule('/posts', 'all', self.all, methods=['GET'])
    self.blueprint.add_url_rule('/posts/<int:post_id>', 'retrieve', self.retrieve, methods=['GET'])
    self.blueprint.add_url_rule('/posts/<int:post_id>', 'update', self.update, methods=['PUT'])
    self.blueprint.add_url_rule('/posts/<int:post_id>', 'delete', self.delete, methods=['DELETE'])

  def create(self):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json

    title = data.get("title", "").strip()
    content = data.get("content", "").strip()

    if not title or not content:
      return jsonify({"error": "Title and content are required"}), 400

    if len(title) > 255:
      return jsonify({"error": "Title cannot exceed 255 characters"}), 400

    post = PostController.create_post(user_authenticated, data)

    if not post:
      return jsonify({"error": "Failed to create post"}), 400

    return jsonify(post.to_dict()), 201

  def all(self):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401

    posts = PostController.get_all_posts(user_authenticated)

    return jsonify([post.to_dict() for post in posts]), 200

  def retrieve(self, post_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    post = PostController.get_post(user_authenticated, post_id)
    
    if post:
      return jsonify(post.to_dict()), 200
    
    return jsonify({"error": "Post not found"}), 404

  def update(self, post_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json

    if "title" in data and len(data["title"]) > 255:
      return jsonify({"error": "Title cannot exceed 255 characters"}), 400

    post = PostController.update_post(user_authenticated, post_id, data)
    
    if post:
      return jsonify(post.to_dict()), 200
    
    return jsonify({"error": "Post not found"}), 404

  def delete(self, post_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    post = PostController.delete_post(user_authenticated, post_id)
    
    if post:
      return jsonify({"message": "Post deleted"}), 200
    
    return jsonify({"error": "Post not found"}), 404

class CommentRoutes:
  def __init__(self):
    self.blueprint = Blueprint('comments', __name__)
    self.blueprint.add_url_rule('/comments/<int:post_id>', 'create', self.create, methods=['POST'])
    self.blueprint.add_url_rule('/comments/<int:post_id>', 'all', self.all, methods=['GET'])
    self.blueprint.add_url_rule('/comments/<int:post_id>/<int:comment_id>', 'update', self.update, methods=['PUT'])
    self.blueprint.add_url_rule('/comments/<int:post_id>/<int:comment_id>', 'delete', self.delete, methods=['DELETE'])

  def create(self, post_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json

    content = data.get("content", "").strip()
    
    if not content:
      return jsonify({"error": "Content is required"}), 400

    if len(content) > 500:
      return jsonify({"error": "Content cannot exceed 500 characters"}), 400

    comment = CommentController.create_comment(user_authenticated, post_id, data)

    if not comment:
      return jsonify({"error": "Failed to create comment"}), 400
    
    return jsonify(comment.to_dict()), 201

  def all(self, post_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    comments = CommentController.get_all_comments(user_authenticated, post_id)

    return jsonify([comment.to_dict() for comment in comments]), 200

  def update(self, post_id, comment_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    comment = CommentController.update_comment(user_authenticated, post_id, comment_id, data)

    if not comment:
      return jsonify({"error": "Failed to update comment"}), 400
    
    return jsonify(comment.to_dict()), 200

  def delete(self, post_id, comment_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    comment = CommentController.delete_comment(user_authenticated, post_id, comment_id)

    if not comment:
      return jsonify({"error": "Failed to delete comment"}), 400
    
    return jsonify({"message": "Comment deleted"}), 200

class FollowRoutes:
  def __init__(self):
    self.blueprint = Blueprint('follows', __name__)
    self.blueprint.add_url_rule('/follows/<int:user_id>', 'follow', self.follow, methods=['POST'])
    self.blueprint.add_url_rule('/follows/<int:user_id>', 'unfollow', self.unfollow, methods=['DELETE'])
    self.blueprint.add_url_rule('/follows/followers/<int:user_id>', 'followers', self.followers, methods=['GET'])
    self.blueprint.add_url_rule('/follows/following/<int:user_id>', 'following', self.following, methods=['GET'])

  def follow(self, user_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    follow = FollowController.follow_user(user_authenticated, user_id)

    if not follow:
      return jsonify({"error": "Failed to follow user"}), 400
    
    return jsonify(follow.to_dict()), 201

  def unfollow(self, user_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    follow = FollowController.unfollow_user(user_authenticated, user_id)

    if not follow:
      return jsonify({"error": "Failed to unfollow user"}), 400
    
    return jsonify(follow.to_dict()), 200

  def followers(self, user_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    followers = FollowController.get_all_followers(user_id)

    return jsonify([follower.to_dict() for follower in followers]), 200

  def following(self, user_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    following = FollowController.get_all_following(user_id)

    return jsonify([follow.to_dict() for follow in following]), 200

class LikeRoutes:
  def __init__(self):
    self.blueprint = Blueprint('likes', __name__)
    self.blueprint.add_url_rule('/likes/<int:post_id>', 'add', self.add, methods=['POST'])
    self.blueprint.add_url_rule('/likes/<int:post_id>', 'remove', self.remove, methods=['DELETE'])
    self.blueprint.add_url_rule('/likes/<int:post_id>', 'all', self.all, methods=['GET'])

  def add(self, post_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    like = LikeController.like_post(user_authenticated, post_id)

    if not like:
      return jsonify({"error": "Failed to like post"}), 400
    
    return jsonify(like.to_dict()), 201

  def remove(self, post_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    like = LikeController.unlike_post(user_authenticated, post_id)

    if not like:
      return jsonify({"error": "Failed to unlike post"}), 400
    
    return jsonify(like.to_dict()), 200

  def all(self, post_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    likes = LikeController.get_all_likes(post_id)

    return jsonify([like.to_dict() for like in likes]), 200

class ImageRoutes:
  def __init__(self):
    self.blueprint = Blueprint('images', __name__)
    self.blueprint.add_url_rule('/images/<int:post_id>', 'upload', self.upload, methods=['POST'])
    self.blueprint.add_url_rule('/images/<int:post_id>', 'all', self.all, methods=['GET'])
    self.blueprint.add_url_rule('/images/<int:post_id>/<int:image_id>', 'delete', self.delete, methods=['DELETE'])

  def upload(self, post_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    if 'file' not in request.files:
      return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
      return jsonify({"error": "No selected file"}), 400
    
    result = ImageController.upload_image(post_id, file)
    
    if result:
      return jsonify({"message": "Image uploaded successfully", "image": result.to_dict()}), 201
    
    return jsonify({"error": "Failed to upload image"}), 500

  def all(self, post_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    images = ImageController.get_all_images(post_id)

    return jsonify([image.to_dict() for image in images]), 200

  def delete(self, post_id, image_id):
    user_authenticated = require_auth()

    if not user_authenticated:
      return jsonify({"error": "Unauthorized"}), 401
    
    image = ImageController.delete_image(post_id, image_id)
    
    if image:
      return jsonify({"message": "Image deleted successfully"}), 200
    
    return jsonify({"error": "Failed to delete image"}), 404

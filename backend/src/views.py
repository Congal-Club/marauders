from flask import Blueprint, jsonify, request

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
    user = UserController.create_user(data)
    
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
    user, error = AuthController.signup(data)
    
    if error:
      return jsonify({"error": error}), 400
    
    return jsonify(user.to_dict()), 201

  def signin(self):
    data = request.json
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
    pass

  def all(self, post_id):
    pass

  def update(self, post_id, comment_id):
    pass

  def delete(self, post_id, comment_id):
    pass

class FollowRoutes:
  def __init__(self):
    self.blueprint = Blueprint('follows', __name__)
    self.blueprint.add_url_rule('/follows/<int:user_id>', 'follow', self.follow, methods=['POST'])
    self.blueprint.add_url_rule('/follows/<int:user_id>', 'unfollow', self.unfollow, methods=['DELETE'])
    self.blueprint.add_url_rule('/follows/<int:user_id>', 'followers', self.followers, methods=['GET'])
    self.blueprint.add_url_rule('/follows/<int:user_id>', 'following', self.following, methods=['GET'])

  def follow(self, user_id):
    pass

  def unfollow(self, user_id):
    pass

  def followers(self, user_id):
    pass

  def following(self, user_id):
    pass

class LikeRoutes:
  def __init__(self):
    self.blueprint = Blueprint('likes', __name__)
    self.blueprint.add_url_rule('/likes/<int:post_id>', 'add', self.add, methods=['POST'])
    self.blueprint.add_url_rule('/likes/<int:post_id>', 'remove', self.remove, methods=['DELETE'])
    self.blueprint.add_url_rule('/likes/<int:post_id>', 'all', self.all, methods=['GET'])

  def add(self, post_id):
    pass

  def remove(self, post_id):
    pass

  def all(self, post_id):
    pass

class ImageRoutes:
  def __init__(self):
    self.blueprint = Blueprint('images', __name__)
    self.blueprint.add_url_rule('/images/<int:post_id>', 'upload', self.upload, methods=['POST'])
    self.blueprint.add_url_rule('/images/<int:post_id>', 'all', self.all, methods=['GET'])
    self.blueprint.add_url_rule('/images/<int:post_id>/<int:image_id>', 'delete', self.delete, methods=['DELETE'])

  def upload(self, post_id):
    pass

  def all(self, post_id):
    pass

  def delete(self, post_id, image_id):
    pass

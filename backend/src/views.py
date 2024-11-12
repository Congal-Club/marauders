from flask import Blueprint, jsonify, request

from .controller import AuthController, UserController
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
    user_id = require_auth()

    if not user_id:
      return jsonify({"error": "Unauthorized"}), 401
    
    AuthController.signout(user_id)
    
    return jsonify({"message": "Signed out successfully"}), 200

  def change_password(self):
    user_id = require_auth()

    if not user_id:
      return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    user, error = AuthController.change_password(user_id, data)
    
    if error:
      return jsonify({"error": error}), 400
    
    return jsonify({"message": "Password updated successfully"}), 200

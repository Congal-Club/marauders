from flask import Blueprint, jsonify, request
from .controller import UserController

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

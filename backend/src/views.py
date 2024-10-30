from flask import Blueprint, jsonify, request, abort
from .controller import create_user, get_all_users, get_user, update_user, delete_user

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/users', methods=['POST'])
def create():
  data = request.json
  user = create_user(data)

  return jsonify(user.to_dict()), 201

@user_blueprint.route('/users', methods=['GET'])
def all():
  users = get_all_users()

  return jsonify([user.to_dict() for user in users]), 200

@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
def retrieve(user_id):
  user = get_user(user_id)

  if user:
    return jsonify(user.to_dict()), 200
  
  return jsonify({"error": "User not found"}), 404

@user_blueprint.route('/users/<int:user_id>', methods=['PUT'])
def update(user_id):
  data = request.json
  user = update_user(user_id, data)

  if user:
    return jsonify(user.to_dict()), 200
  
  return jsonify({"error": "User not found"}), 404

@user_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
def delete(user_id):
  user = delete_user(user_id)

  if user:
    return jsonify({"message": "User deleted"}), 200
  
  return jsonify({"error": "User not found"}), 404

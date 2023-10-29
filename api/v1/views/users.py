#!/usr/bin/python3
""" Handles all default RESTful API action
"""
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
	"""
	Get all users from the storage and return them as a JSON response.
	"""
	users = storage.all("User")
	users_list = []
	for user in users.values():
		users_list.append(user.to_dict())
	return jsonify(users_list), 200


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
	"""
	Get a user by its ID.
	"""
	user = storage.get(User, user_id)
	if not user:
		abort(404, description="User not found")
	return jsonify(user.to_dict()), 200


@app_views.route(
	'/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
	"""
	Deletes a user from the database.
	"""
	user = storage.get(User, user_id)
	if not user:
		abort(404)
	user.delete()
	storage.save()
	return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def post_user():
	"""
	Creates a new user.
	"""
	user = request.get_json()
	if not user:
		abort(400, description="Not a JSON")
	if 'email' not in user:
		abort(400, description="Missing email")
	if 'password' not in user:
		abort(400, description="Missing password")
	user = User(**user)
	user.save()
	return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def put_user(user_id):
	"""
	Updates an existing user.
	"""
	user = storage.get(User, user_id)
	if not user:
		abort(404)
	user = request.get_json()
	if not user:
		abort(400, description="Not a JSON")
	for key, value in user.items():
		if key not in ['id', 'email', 'created_at', 'updated_at']:
			setattr(user, key, value)
	user.save()
	return jsonify(user.to_dict()), 200

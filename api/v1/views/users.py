#!/usr/bin/python3
"""
New view for User object that handles all default RESTFul API actions
"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage, User

# Route to retrieve a list of all User objects
@app_views.route('/users', methods=['GET'])
def get_users():
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)

# Route to retrieve a specific User object by user_id
@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())

# Route to delete a specific User object by user_id
@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200

# Route to create a new User object
@app_views.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    
    new_user = User(**data)
    new_user.save()
    
    return jsonify(new_user.to_dict()), 201

# Route to update a specific User object by user_id
@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    
    # Ignore keys: id, email, created_at, updated_at
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    
    user.save()
    
    return jsonify(user.to_dict()), 200

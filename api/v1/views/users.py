#!/usr/bin/python3
"""users"""
from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users')
def list_users():
    '''Retrieves a list of all User objects'''
    users = [user.to_dict() for user in storage.all("User").values()]
    return jsonify(users)


@app_views.route('/users/<user_id>')
def get_user(user_id):
    '''Retrieves a User object'''
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    '''Deletes'''
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    '''Creates'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    email = request.json.get('email')
    password = request.json.get('password')
    if not email:
        abort(400, 'Missing email')
    if not password:
        abort(400, 'Missing password')
    new_user = User(email=email, password=password)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    '''Updates'''
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    storage.save()
    return jsonify(user.to_dict()), 200

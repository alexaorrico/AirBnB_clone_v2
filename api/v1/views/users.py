#!/usr/bin/python3
"users view"
from flask import jsonify, abort, request

from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'])
def users():
    "Retrieves list of all users"
    return jsonify([user.to_dict() for user in storage.all(User).values()])


@app_views.route('/users/<id>', methods=['GET'])
def user_by_id(id):
    "display user by id"
    user = storage.get(User, id)
    if user:
        return user.to_dict()
    return abort(404)


@app_views.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    """delete a user by its id"""
    user = storage.get(User, id)
    if user:
        storage.delete(user)
        storage.save()
        return {}
    return abort(404)


@app_views.route('/users', methods=['POST'])
def create_user():
    """create a new user"""
    if request.is_json:
        data = request.get_json()
        if not data.get('email'):
            abort(400, 'Missing email')
        if not data.get('password'):
            abort(400, 'Missing password')
        new_user = User(**data)
        new_user.save()
        return new_user.to_dict(), 201

    abort(400, 'Not a JSON')


@app_views.route('/users/<id>', methods=['PUT'])
def update_user(id):
    """update a user by its id"""
    user = storage.get(User, id)
    if not user:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for k, v in data.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    storage.save()
    return user.to_dict()

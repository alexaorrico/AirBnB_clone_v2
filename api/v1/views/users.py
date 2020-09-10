#!/usr/bin/python3
"""
Task 10
Create a new view for User objects
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/api/v1/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Retrieves the list of all User objects"""
    all_users = []
    for user in storage.all('User').values():
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/api/v1/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_user(user_id):
    """Retrieves a User object"""
    try:
        user = storage.get('User', user_id).to_dict()
        return jsonify(user)
    except:
        abort(404)


@app_views.route('/api/v1/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get('User', user_id)
    if user:
        user.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/api/v1/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Creates a User"""
    user_list = request.get_json()
    if not user_list:
        abort(400, {'Not a JSON'})
    elif 'email' not in user_list:
        abort(400, {'Missing email'})
    elif 'password' not in user_list:
        abort(400, {'Missing password'})
    new_user = User(**user_list)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/api/v1/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User"""
    update_obj = request.get_json()
    if not update_obj:
        abort(400, {'Not a JSON'})
    my_user = storage.get('User', user_id)
    if not this_user:
        abort(404)
    for key, value in update_attr.items():
        setattr(this_user, key, value)
    storage.save()
    return jsonify(this_user.to_dict())

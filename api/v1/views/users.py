#!/usr/bin/python3
'''
methods and routes for working with user data
'''
from models.user import User
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/user', methods=['GET'], strict_slashes=False)
def all_users():
    '''
    Gets all of the users listed
    '''
    all_users = []
    for i in storage.all("User").values():
        all_users.append(i.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_by_id(user_id):
    '''
    gets the user by user id
    '''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/user/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    '''
    deletes a user if given the id
    '''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return ({}), 200


@app_views.route('/user', methods=['POST'], strict_slashes=False)
def add_user():
    '''
    adds a user to the DB
    '''
    user = request.get_json()
    if user is None:
        abort(400, 'not a JSON')
    if 'email' not in user:
        abort(400, 'Missing email')
    if 'password' not in user:
        abort(400, 'Missing password')
    new_user = User(**user)
    storage.new(new_user)
    storage.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''
    updates a user in the DB
    '''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_info = request.get_json()
    if user_info is None:
        abort(400, 'not a JSON')
    for key, value in user_info.items():
        if key in ['id', 'email', 'created_at', 'updated_at']:
            pass
        else:
            setattr(user, key, value)
    storage.save()
    all_users = user.to_dict()
    return(jsonify(all_users), 200)

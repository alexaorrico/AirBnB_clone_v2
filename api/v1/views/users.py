#!/usr/bin/python3
'''users.py'''
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id=None):
    '''get user'''
    if user_id:
        user = storage.get(User, user_id)
        if user:
            return jsonify(user.to_dict())
        else:
            abort(404)
    all_users = []
    for user in storage.all('User').values():
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    '''delete user'''
    user = storage.get(User, user_id)
    if user:
        user.delete()
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    '''post user'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in request.get_json():
        return jsonify({'error': 'email name'}), 400
    if 'password' not in request.get_json():
        return jsonify({'error': 'password name'}), 400
    user = User(**request.get_json())
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id=None):
    '''UPdate user'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    user = storage.get(User, user_id)
    if user:
        (request.get_json()).pop('id', None)
        (request.get_json()).pop('updated_at', None)
        (request.get_json()).pop('created_at', None)
        (request.get_json()).pop('email', None)
        for key, value in request.get_json().items():
            setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict())
    else:
        abort(404)

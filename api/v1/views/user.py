#!/usr/bin/python3

"""module user"""

from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request

@app_views.route('/users', method=['GET'], strict_slashes=False)
def get_user():
    """

    """
    all_user = storage.all(User).values()
    # store each comm
    result = [amenity.to_dict() for amenity in all_user]
    return jsonify(result)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """

    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    
    result = user.to_dict
    return jsonify(result)

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_id(user_id):
    """

    """
    delete_user = storage.get(User, user_id)
    if delete_user is None:
        abort(404)
    else:
        storage.delete(delete_user)
        storage.save()
    return jsonify({}), 200

@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def new_user():

    posted = request.get_json()

    if posted is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in posted:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in posted:
        return jsonify({'error': 'Missing password'}), 400
    return jsonify({}), 201

@app_views.route('/users/<user_id>', method='PUT', strict_slashes=False)
def update_user(user_id):
    body = request.get_json()
    if body is None:
        return jsonify({'error': 'Not a JSON'}), 400
    
    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    else:
        ignore = ['id', 'email', 'created_at', 'updated_at']
        for key, value in body.items():
            if key not in ignore:
                setattr(user, key, value)
            else:
                pass
        user.save()
        return jsonify(user.to_dict()), 200
    
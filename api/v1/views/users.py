#!/usr/bin/python3
"""defines the view for user objects"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, request, make_response, jsonify


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users_get(user_id=None):
    """returns all user objects"""
    return [obj.to_dict() for obj in storage.all('User').values()]


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    """creates a new user object"""
    post_data = request.get_json(silent=True)
    if post_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in post_data.keys():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in post_data.keys():
        return make_response(jsonify({'error': 'Missing password'}),
                             400)
    new_user = User(**post_data)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_get_one(user_id):
    """returns specified user"""
    obj = storage.get(User, user_id)
    if obj is not None:
        return obj.to_dict()
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def user_delete(user_id):
    """deletes a user object"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_put(user_id):
    """updates a user object"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    post_data = request.get_json(silent=True)
    if post_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, val in post_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)

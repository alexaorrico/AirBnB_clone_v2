#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort
from models.user import User
from models import storage
from flask import*



@app_views.route('/users', strict_slashes=False)
def list_users():
    """list of users"""
    users = storage.all(User)
    return jsonify(
        [am.to_dict() for user in users.values()]
            )

@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    return jsonify({})

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    get_json = request.get_json()
    if get_json is None:
        abort(404, 'Not a JSON')
    if get_json['email'] is None:
        abort(404, 'Missing email')
    if get_json['password'] is None:
        abort(404, 'Missing password')

    new_user = User(**get_json)
    new_user.save()
    return jsonify(new_user.to_dict())

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort('404')
    if request.get_json() is None:
        abort('404', 'Not a JSON')
    update = request.get_json()
    for key, value in update.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at' or key != 'email':
            setattr(user, key,value)
    user.save()
    return jsonify(user.to_dict()), 200

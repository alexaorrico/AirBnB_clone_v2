#!/usr/bin/python3
"""dont trust the user"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """get em"""
    lizt = []
    users = storage.all(User).values()
    for user in users:
        lizt.append(user.to_dict())
    return jsonify(lizt)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_a_user(user_id):
    """get one"""
    users = storage.get(User, user_id)
    return jsonify((users.to_dict()) if users else abort(404))


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_a_user(user_id):
    """remove one"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    storage.delete(users)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_a_user():
    """create a user"""
    req = request.get_json()
    if req is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    key = 'email'
    if key not in req:
        return make_response(jsonify({"error": "Missing email"}), 400)
    key = 'password'
    if key not in req:
        return make_response(jsonify({"error": "Missing password"}), 400)
    new_user = User(**req)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_a_user(user_id):
    """ this method updates a user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    req = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    for k, value in req.items():
        if k not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, k, value)
    user.save()
    return jsonify(user.to_dict())

#!/usr/bin/python3
"""User module """
from models.user import User
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route("/users")
def all_users():
    """Returns a list of Users"""

    all_users = []

    for user in storage.all("User").values():
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/user_id>')
def get_method_user(user_id):
    """Returns an instance of the specified user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def del_method_user(user_id):
    """deletes user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}, 200))


@app_views.route('/users', methods=['POST'])
def create_user():
    """creates user"""

    if not request.get_json():
        return abort(400, description="Not a JSON")

    if not request.get_json().get('email'):
        return abort(400, description="Missing email")

    if not request.get_json().get('password'):
        return abort(400, description="Missing password")

    user = User()
    user.email = request.get_json().get['email']
    user.password = request.get_json(),get['password']
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """updates user method"""
    if not request.get_json():
        return abort(400, description="Not a JSON")

    user = storage.get("Amenity", amenity_id)

    if user is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(user, key, value)
    storage.save()

    return make_response(jsonify(user.to_dict(), 200))

#!/usr/bin/python3
"""Handles the user view
"""

# from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.user import User
from models.city import City


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Gets the dict containing all the users
    """
    users = storage.all("User")
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """Gets a user by its ID
    """
    user = storage.get("User", user_id)
    if user is not None:
        return jsonify(user.to_dict())
    else:
        return abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a user
    """
    user = storage.get("User", user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        return abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates an user
    """
    got_json = request.get_json()
    if not got_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in got_json:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in got_json:
        return make_response(jsonify({"error": "Missing password"}), 400)
    new_user = User(**got_json)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)



@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates a user
    """
    got_json = request.get_json()
    if not got_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user = storage.get("User", user_id)
    if user:
        for key, val in got_json.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, val)
            storage.save()
        return make_response(jsonify(user.to_dict()), 200)
    else:
        return abort(404)

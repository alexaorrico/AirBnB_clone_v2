#!/usr/bin/python3
"""Users API"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False,
                 methods=['GET'])
@app_views.route("/users/<string:user_id>", strict_slashes=False,
                 methods=['GET'])
def get_users(user_id=None):
    """Retrieves the list of all User objects or a User"""

    if user_id is not None:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        return jsonify(user.to_dict())
    users = list(storage.all(User).values())
    users = [user.to_dict() for user in users]
    return jsonify(users)


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object"""

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    return jsonify({})


@app_views.route("/users", strict_slashes=False,
                 methods=['POST'])
def create_user():
    """Creates a User"""

    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    email = data.get("email", None)
    password = data.get("password", None)
    first_name = data.get("first_name", None)
    last_name = data.get("last_name", None)
    if email is None:
        abort(400, description="Missing email")
    if password is None:
        abort(400, description="Missing password")

    user = User(email=email, password=password)
    if type(first_name) is str and first_name != '':
        user.first_name = first_name
    if type(last_name) is str and last_name != '':
        user.last_name = last_name
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<string:user_id>", strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    """Updates a User object"""

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    data = {k: v for k, v in data.items() if k != 'id' and
            k != 'created_at' and k != 'updated_at' and
            k != 'email'}
    for k, v in data.items():
        setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200

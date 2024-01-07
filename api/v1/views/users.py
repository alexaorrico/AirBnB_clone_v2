#!/usr/bin/python3
"""
contains endpoints(routes) for user objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User


@app_views.route("/users", strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects:
    """
    objs = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(objs)


@app_views.route("/users/<string:user_id>", strict_slashes=False)
def get_user(user_id):
    """
    Retrieves an User
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", strict_slashes=False,
                 methods=['DELETE'])
def del_user(user_id):
    """
    Deletes an User object
    """
    user = storage.get(User, user_id)
    if user:
        user.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/users/", strict_slashes=False,
                 methods=['POST'])
def create_user():
    """
    Creates an User instance
    """
    valid_json = request.get_json()

    if valid_json is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password'not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)

    obj = User(**valid_json)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/users/<string:user_id>", strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    """
    Updates an User object
    """
    user = storage.get(User, user_id)
    valid_json = request.get_json()

    if not user:
        abort(404)

    if valid_json is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in valid_json.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)

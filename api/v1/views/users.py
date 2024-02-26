#!/usr/bin/python3
""" Routes for handling User objects """
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """
    Gets all User objects
    """
    users_list = []
    user_objects = storage.all(User)
    for obj in user_objects.values():
        users_list.append(obj.to_dict())

    return jsonify(users_list)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """
    Creates a new User
    """
    user_json = request.get_json(silent=True)
    if not user_json:
        abort(400, 'Not a JSON')
    if "email" not in user_json:
        abort(400, 'Missing email')
    if "password" not in user_json:
        abort(400, 'Missing password')

    new_user = User(**user_json)
    new_user.save()

    return jsonify(new_user.to_dict())


@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def get_user_by_id(user_id):
    """
    Get a specific User object by ID.
    """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    Update a specific User object by ID.
    """
    user_json = request.get_json(silent=True)
    if not user_json:
        abort(400, 'Not a JSON')

    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)

    for key, val in user_json.items():
        if key != 'id' and key != 'email' and key != 'created_at' and key != 'updated_at':
            setattr(user_obj, key, val)

    user_obj.save()

    return jsonify(user_obj.to_dict())


@app_views.route("/users/<user_id>",  methods=["DELETE"], strict_slashes=False)
def delete_user_by_id(user_id):
    """
    Deletes User by id.
    """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)

    storage.delete(user_obj)
    storage.save()

    return jsonify({})


#!/usr/bin/python3
""" Routes for handling User objects """
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """
    gets all User objects
    """
    users_list = []
    user_object = storage.all("User")
    for obj in user_object.values():
        users_list.append(obj.to_json())

    return jsonify(users_list)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """
    creates a new User route
    """
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, 'Not a JSON')
    if "email" not in user_json:
        abort(400, 'Missing email')
    if "password" not in user_json:
        abort(400, 'Missing password')

    new_user = User(**user_json)
    new_user.save()
    rsponse = jsonify(new_user.to_json())
    rsponse.status_code = 201

    return rsponse


@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def get_user_by_id(user_id):
    """
    Get a specific User object by ID.
    """

    obj_fetched = storage.get("User", str(user_id))

    if obj_fetched is None:
        abort(404)

    return jsonify(obj_fetched.to_json())


@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def get_user_put(user_id):
    """
    Update a specific User object by ID.
    """
    user_json = request.get_json(silent=True)

    if user_json is None:
        abort(400, 'Not a JSON')

    obj_fetched = storage.get("User", str(user_id))

    if obj_fetched is None:
        abort(404)

    for key, val in user_json.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(obj_fetched, key, val)

    obj_fetched.save()

    return jsonify(obj_fetched.to_json())


@app_views.route("/users/<user_id>",  methods=["DELETE"], strict_slashes=False)
def delete_user_by_id(user_id):
    """
    Deletes User by id.
    """

    obj_fetched = storage.get("User", str(user_id))

    if obj_fetched is None:
        abort(404)

    storage.delete(obj_fetched)
    storage.save()

    return jsonify({})

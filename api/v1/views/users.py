#!/usr/bin/python3
""" Users """
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/api/v1/users", methods=["GET"], strict_slashes=False)
def user_get_all():
    """
    retrieves all User objects
    :return: json of all users
    """
    user_list = []
    user_obj = storage.all("User")
    for obj in user_obj.values():
        user_list.append(obj.to_json())

    return jsonify(user_list)


@app_views.route("/api/v1/users/<user_id>", methods=["GET"], strict_slashes=False)
def user_get(user_id):
    """
    retrieves a User object by ID
    :param user_id: ID of the User object to retrieve
    :return: JSON representation of the User object
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route("/api/v1/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def user_delete(user_id):
    """
    deletes a User object by ID
    :param user_id: ID of the User object to delete
    :return: empty dictionary with status code 200
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/api/v1/users", methods=["POST"], strict_slashes=False)
def user_create():
    """
    create user route
    :return: newly created user obj
    """
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, "Not a JSON")
    if "email" not in user_json:
        abort(400, "Missing email")
    if "password" not in user_json:
        abort(400, "Missing password")

    new_user = User(**user_json)
    new_user.save()
    resp = jsonify(new_user.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/api/v1/users/<user_id>", methods=["PUT"], strict_slashes=False)
def user_update(user_id):
    """
    updates a User object by ID
    :param user_id: ID of the User object to update
    :return: updated User object with status code 200
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, "Not a JSON")

    # Update the User object with the provided key-value pairs
    # Ignore keys: id, email, created_at, and updated_at
    for key, value in user_json.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_json()), 200

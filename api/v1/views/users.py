#!/usr/bin/python3
"""
Users view
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
def get_users():
    """Retrieves the list of all Users objects"""
    user_list = [
        user.to_dict() for user in storage.all("User").values()
        ]
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a specific User object by ID"""
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a specific User object by ID"""
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return jsonify({})


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a new User object"""
    user_data = request.get_json(silent=True)
    if user_data is None:
        abort(400, "Not a JSON")

    if "email" not in user_data:
        abort(400, "Missing email")

    if "password" not in user_data:
        abort(400, "Missing password")

    new_user = User(**user_data)
    new_user.save()

    resp = jsonify(new_user.to_dict())
    resp.status_code = 201
    return resp


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a specific User object by ID"""
    user_data = request.get_json(silent=True)
    if user_data is None:
        abort(400, "Not a JSON")

    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)

    for key, value in user_data.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(user_obj, key, value)

    user_obj.save()

    resp = jsonify(user_obj.to_dict())
    resp.status_code = 200
    return resp

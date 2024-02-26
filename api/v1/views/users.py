#!/usr/bin/python3
"""script that handles User objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get_all():
    """retrieves all User objects"""
    list_of_users = []
    objs = storage.all("User")
    for obj in objs.values():
        list_of_users.append(obj.to_dict())
    return jsonify(list_of_users)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_create():
    """create user route"""
    json_users = request.get_json(silent=True)
    if json_users is None:
        abort(400, 'Not a JSON')
    if "email" not in json_users:
        abort(400, 'Missing email')
    if "password" not in json_users:
        abort(400, 'Missing password')
    new_user = User(**json_users)
    new_user.save()
    response = jsonify(new_user.to_dict())
    response.status_code = 201
    return response


@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """gets a specific User object by ID
    Args:
        user_id: user object id"""
    objs = storage.get("User", str(user_id))
    if objs is None:
        abort(404)
    return jsonify(objs.to_dict())


@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def user_put(user_id):
    """updates specific User object by ID
    Args:
        user_id: user object ID"""
    json_users = request.get_json(silent=True)
    if json_users is None:
        abort(400, 'Not a JSON')
    objs = storage.get("User", str(user_id))
    if objs is None:
        abort(404)
    for key, val in json_users.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(objs, key, val)
    objs.save()
    return jsonify(objs.to_dict())


@app_views.route("/users/<user_id>",  methods=["DELETE"], strict_slashes=False)
def user_delete_by_id(user_id):
    """deletes User by id
    Args:
        user_id: user object id"""
    objs = storage.get("User", str(user_id))
    if objs is None:
        abort(404)
    storage.delete(objs)
    storage.save()
    return jsonify({})

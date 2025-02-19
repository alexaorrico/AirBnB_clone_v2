#!/usr/bin/python3
""" handles all default RESTFul API actions"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users_all():
    """Retrieves the list of all User objects """
    user_l = []
    user_o = storage.all("User")
    for obj in user_o.values():
        user_l.append(obj.to_dict())

    return jsonify(user_l)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def user_delete(user_id):
    """Deletes a User object"""
    d_obj = storage.get("User", str(user_id))
    if d_obj is None:
        abort(404)

    storage.delete(d_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_create():
    """Creates a User"""
    user_j = request.get_json(silent=True)
    if user_j is None:
        abort(400, description='Not a JSON')
    if "email" not in user_j:
        abort(400, description='Missing email')
    if "password" not in user_j:
        abort(400, description='Missing password')
    new_user = User(**user_j)
    new_user.save()
    repo = jsonify(new_user.to_dict())
    repo.status_code = 201

    return repo


@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def user_update(user_id):
    """update a user"""
    user_j = request.get_json(silent=True)
    if user_j is None:
        abort(400, 'Not a JSON')
    d_obj = storage.get("User", str(user_id))
    if d_obj is None:
        abort(404)
    for key, val in user_j.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(d_obj, key, val)
    d_obj.save()
    return jsonify(d_obj.to_dict())

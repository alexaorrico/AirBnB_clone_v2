#!/usr/bin/python3
"""
new view for User objects that handles all default RESTFul API actions
"""
from flask import jsonify, request, abort
from . import app_views, storage, User
from hashlib import md5

pl = (
    "email",
    "password",
    "first_name",
    "last_name"
    )


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
def all_users():
    """Adds a list of users to the list of users"""
    if request.method == "GET":
        return jsonify([list.to_dict() for list in storage.all(User).values()])
    else:
        data = request.get_json(silent=True)
        if request.is_json and data is not None:
            load = {key: str(value) for key, value in data.items()
                    if key in pl}
            for key in pl[:2]:
                if not load.get(key, None):
                    abort(400, description="Missing " + key)
            added_user = User(**load)
            storage.new(added_user), storage.save()
            return jsonify(added_user.to_dict()), 201
        abort(400, description="Not a JSON")


@app_views.route("/users/<user_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def one_user(user_id):
    """Removes specified user from list of users matching specified user_id"""
    deleted_user = storage.get(User, str(user_id))
    if not deleted_user:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify(deleted_user.to_dict())
    elif request.method == "DELETE":
        storage.delete(deleted_user), storage.save()
        return jsonify({})
    else:
        data = request.get_json(silent=True)
        if request.is_json and data is not None:
            load = {key: str(value) for key, value in data.items()
                    if key in pl[1:]}
            if load.get("password", None):
                loading = load.get("password")
                load.update({"password": md5(bytes(loading,
                                                   'utf-8')).hexdigest()})
            [setattr(deleted_user, key, str(value))
             for key, value in load.items()]
            deleted_user.save()
            return jsonify(deleted_user.to_dict()), 200
        abort(400, description="Not a JSON")

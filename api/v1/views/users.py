#!/usr/bin/python3
"""
Create a new view for Users objects
that handles all default RESTFul API actions
"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route("/users",
                 methods=["GET"],
                 strict_slashes=False)
def get_user():
    """ List all users """
    get_users = storage.all(User).values()
    list_users = []
    for elm in get_users:
            list_users.append(elm.to_dict())
    return jsonify(list_users)


@app_views.route("/users/<user_id>",
                 methods=["GET"],
                 strict_slashes=False)
def get_id_users(user_id=None):
    """ Return a user object """
    user_ob = storage.get(User, user_id)
    if user_ob:
        return jsonify(user_ob.to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id=None):
    """ Delete A User """
    user_ob = storage.get(User, user_id)
    if user_ob:
        storage.delete(user_ob)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users",
                 methods=["POST"],
                 strict_slashes=False)
def post_user():
    """ Create an User object """
    if not request.get_json():
        abort(400, "Not a JSON")
    if "email" not in request.get_json():
        abort(400, "Missing email")
    if "password" not in request.get_json():
        abort(400, "Missing password")
    data = request.get_json()
    user_ob = User(**data)
    user_ob.save()
    return (jsonify(user_ob.to_dict()), 201)


@app_views.route("/users/<user_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def put_user(user_id):
    """ Update a User object """
    up_date = storage.get(User, user_id)
    data = request.get_json()
    if up_date:
        if data:
            for k, v in data.items():
                ignore = ["id", "email", "created_at", "updated_at"]
                if k != ignore:
                    setattr(up_date, k, v)
                up_date.save()
                return jsonify(up_date.to_dict())
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)

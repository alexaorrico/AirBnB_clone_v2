#!/usr/bin/python3
"""
File that configures the routes of users
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage
from sqlalchemy.exc import IntegrityError


@app_views.route("/users", strict_slashes=False)
@app_views.route("/users/<user_id>", strict_slashes=False)
def get_users(user_id=None):
    """
    Route to get users
    """
    list_obj = []
    if not user_id:
        for val in storage.all("User").values():
            list_obj.append(val.to_dict())
        return jsonify(list_obj)
    user_obj = storage.get("User", user_id)
    if user_obj:
        return jsonify(user_obj.to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    """
    deletes a User object
    """
    user_obj = storage.get("User", user_id)
    if user_obj is not None:
        user_obj.delete()
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def post_user():
    """
    Route that create a new User
    """
    try:
        obj_data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if "email" not in request.get_json():
        abort(400, "Missing email")
    if "password" not in request.get_json():
        abort(400, "Missing password")
    obj_data = request.get_json()
    if obj_data:
        new_user_obj = User(**obj_data)
        new_user_obj.save()
        return (jsonify(new_user_obj.to_dict()), 201)
    else:
        abort(400, "Not a JSON")


@app_views.route("/users", methods=["PUT"], strict_slashes=False)
@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def put_user(user_id=None):
    """
    Route that update an User
    """
    user_obj = storage.get("User", user_id)
    if user_obj:
        try:
            data = request.get_json()
        except Exception:
            abort(400, "Not a JSON")
        if data:
            for key, value in data.items():
                if (key != "id" and key != "created_at" and
                        key != "updated_at" and key != "email"):
                    setattr(user_obj, key, value)
            user_obj.save()
            return (jsonify(user_obj.to_dict()), 200)
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)

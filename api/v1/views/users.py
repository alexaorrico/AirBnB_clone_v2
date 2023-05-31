#!/usr/bin/python3
"""restful API functions for User"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import request, jsonify, abort


@app_views.route(
        "/users", strict_slashes=False, methods=["GET", "POST"])
@app_views.route(
        "/users/<user_id>", strict_slashes=False,
        methods=["DELETE", "PUT", "GET"])
def user_end_points(user_id=None):
    """to get users"""
    obj_users = storage.all(User)
    if not user_id:
        if request.method == "GET":
            users = [user.to_dict() for user in obj_users.values()]
            return jsonify(users), 200

        elif request.method == "POST":
            data = request.get_json()
            if not data:
                abort(400, "Not a JSON")
            if not data.get("email"):
                abort(400, "Missing email")
            if not data.get("password"):
                abort(400, "Missing password")
            else:
                new_user = User(**data)
                new_user.save()
                return jsonify(new_user.to_dict()), 201
    else:
        user = storage.get(User, user_id)
        if not user:
            abort(404)

        if request.method == "GET":
            return jsonify(user.to_dict()), 200

        elif request.method == "DELETE":
            storage.delete(user)
            storage.save()
            return jsonify({}), 200

        elif request.method == "PUT":
            data = request.get_json()
            if not data:
                abort(400, "Not a JSON")

            ignore_keys = ['id', 'email', 'created_at', 'updated_at']
            for key, value in data.items():
                if key not in ignore_keys:
                    setattr(user, key, value)
            user.save()
            return jsonify(user.to_dict()), 200

    abort(404)

#!/usr/bin/python3
"""this is a test string"""

from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=["GET", "POST"])
def users_base():
    """this is a test string"""
    if request.method == "GET":
        out = []
        for user in storage.all("User").values():
            out.append(user.to_dict())
        return jsonify(out)
    if request.method == "POST":
        if not request.is_json:
            return "Not a JSON", 400
        out = User(**request.get_json())
        if "email" not in out.to_dict().keys():
            return "Missing email", 400
        if "password" not in out.to_dict().keys():
            return "Missing password", 400
        out.save()
        return out.to_dict(), 201


@app_views.route("/users/<u_id>",
                 strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def users_id(u_id):
    """this is a test string"""
    if request.method == "GET":
        for user in storage.all("User").values():
            if user.id == u_id:
                return user.to_dict()
        abort(404)
    if request.method == "DELETE":
        for user in storage.all("User").values():
            if user.id == u_id:
                user.delete()
                storage.save()
                return {}, 200
        abort(404)
    if request.method == "PUT":
        for user in storage.all("User").values():
            if user.id == u_id:
                if not request.is_json:
                    return "Not a JSON", 400
                for k, v in request.get_json().items():
                    setattr(user, k, v)
                storage.save()
                return user.to_dict()
        abort(404)

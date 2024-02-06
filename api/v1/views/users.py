#!/usr/bin/python3
""" This file contains the views implementation of
users request as blueprint"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
import json


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
@app_views.route(
            "/users/<user_id>",
            methods=["GET", "DELETE", "PUT"],
            strict_slashes=False
            )
def users_view(user_id=None):
    """ View function to retrieve user
    objects"""
    if request.method == "GET" and user_id is None:
        user_objects = storage.all(User).values()
        object_returned = [
                    obj.to_dict() for obj in user_objects
                    ]
        return jsonify(object_returned), 200
    if request.method == "POST" and user_id is None:
        if not request.is_json:
            #  abort(400, description="Not a JSON")
            return jsonify({"error": "Not a JSON"}), 400
        input_data = request.get_json()   # Not always dict.
        if "email" not in input_data:
            #  abort(400, "Missing email")
            return jsonify({"error": "Missing email"}), 400
        elif "password" not in input_data:
            #  abort(400, jsonify({"error": "Missing password"}))
            return jsonify({"error": "Missing password"}), 400
        else:
            new_user = User(**input_data)
            storage.new(new_user)
            storage.save()
            return jsonify(new_user.to_dict()), 201
    if user_id is not None:
        user_object = storage.get(User, user_id)
        if request.method == "GET":
            if user_object is None:
                abort(404)
            return jsonify(user_object.to_dict()), 200
        if request.method == "DELETE":
            if user_object is None:
                abort(404)
            storage.delete(user_object)
            storage.save()
            return jsonify({}), 200
        if request.method == "PUT":
            if user_object is None:
                abort(404)
            if not request.is_json:
                #  abort(400, description=jsonify({"error": "Not a JSON"}))
                return jsonify({"error": "Not a JSON"}), 400
            user_update_data = request.get_json()
            for k, v in user_update_data.items():
                if k not in [
                        "id", "email", "created_at", "updated_at"
                        ]:
                    setattr(user_object, k, v)
            user_object.save()
            return jsonify(user_object.to_dict()), 200

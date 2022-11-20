#!/usr/bin/python3
"""Contains fuction thet handles all requests to /users endpoints."""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, user


@app_views.route("/users",
                 strict_slashes=False,
                 defaults={'user_id': None},
                 methods=['GET', 'POST'])
@app_views.route("/users/<user_id>",
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def user_endpoint(user_id):
    """Handles all requests to /users endpoints."""
    if request.method == "GET":
        if user_id is None:
            return [obj.to_dict() for obj in storage.all(user.User).values()]
        elif user_id is not None:
            u_obj = storage.get("User", user_id)
            if not u_obj:
                abort(404)
            return jfonify(obj.to_dict())
    elif request.method == "POST":
        try:
            post_data = request.get_json()
        except Exception:
            return make_response("Not a JSON", 400)
        if "email" not in post_data:
            return make_response("Missing email", 400)
        if "password" not in post_data:
            return make_response("Missing password", 400)
        new_user = user.User()
        new_user.email = post_data['email']
        new_user.password = post_data['password']
        new_user.save()
        return make_response(new_user.to_dict(), 201)
    elif request.method == "PUT":
        try:
            put_data = request.get_json()
        except Exception:
            return make_response("Not a JSON", 400)
        u_obj = storage.get("User", user_id)
        if not u_obj:
            abort(404)
        for key, value in put_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(u_obj, key, value)
        u_obj.save()
        return make_response(jsonify(u_obj.to_dict()), 200)
        abort(404)
    elif request.method == "DELETE":
        u_obj = storage.get("User", user_id)
        if u_obj is None:
            abort(404)
        u_obj.delete()
        storage.save()
        return (jsonify({}))

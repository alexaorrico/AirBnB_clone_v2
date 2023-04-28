#!/usr/bin/python3

"""handles all default RESTFul API actions for User object"""

from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route("/users", methods=["GET", "POST"])
@app_views.route("/users/<string:user_id>", methods=["GET", "PUT", "DELETE"])
def users(user_id=None):
    """handles all default RESTFul API actions for User object"""

    if user_id:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
            return

    if request.method == "GET":
        if user_id is None:
            users = [user.to_dict() for user in storage.all(User).values()]
            return jsonify(users)
        return jsonify(user.to_dict())

    elif request.method == "DELETE":
        user.delete()
        storage.save()
        return jsonify({})

    elif request.method == "POST":
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        elif "email" not in request.get_json():
            return make_response(jsonify({"error": "Missing email"}), 400)
        elif "password" not in request.get_json():
            return make_response(jsonify({"error": "Missing password"}), 400)
        new_dict = request.get_json()
        new_user = User(**new_dict)
        new_user.save()
        return make_response(jsonify(new_user.to_dict()), 201)

    elif request.method == "PUT":
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        updates = request.get_json()
        for attr, value in updates.items():
            if attr not in ["id", "email", "created_at", "updated_at"]:
                setattr(user, attr, value)
        user.save()
        return make_response(jsonify(user.to_dict()), 200)

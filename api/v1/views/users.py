#!/usr/bin/python3
""" States handler of app """
from api.v1.views import app_views
from flask import jsonify, abort, Response, request, make_response
from json import dumps, loads
from models import storage
from models.user import User


@app_views.route("/users/", methods=["GET"], strict_slashes=False)
def app_route_users1():
    """ GET all users """
    converted_states = []
    all_states = storage.all()
    for values in all_states.values():
        if values.to_dict()["__class__"] == "User":
            converted_states.append(values.to_dict())
    return jsonify(converted_states)


@app_views.route("/users/<users_id>", methods=["GET"], strict_slashes=False)
def app_route_users2(users_id):
    """ GET user from ID """
    search = storage.get("User", users_id)
    if search:
        return jsonify(search.to_dict())
    return abort(404)


@app_views.route("/users/<users_id>", methods=["DELETE"])
def app_route_users3(users_id):
    """ DELETE user from ID """
    search = storage.get("User", users_id)
    if search:
        storage.delete(search)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def app_route_users4():
    """ POST new user """
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    if 'email' not in data:
        return abort(400, "Missing email")
    if 'password' not in data:
        return abort(400, "Missing email")
    user = User(**data)
    user_dict = user.to_dict()
    user.save()
    return jsonify(user_dict), 201


@app_views.route('/users/<users_id>', methods=['PUT'], strict_slashes=False)
def app_route_user5(users_id):
    """ PUT update an user """
    if users_id:
        obj_users = storage.get(User, users_id)
        if obj_users is None:
            return abort(404)
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(obj_users, key, value)
        obj_users.save()
        return make_response(jsonify(obj_users.to_dict()), 200)

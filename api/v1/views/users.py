#!/usr/bin/python3
""" Create a view for the User Objects """


from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route("/users", methods=["GET"])
def all_users():
    """ Retrieve all User objects """
    users = storage.all(User)
    user_list = [user.to_dict() for user in users.values()]
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=["GET"])
def one_user(user_id):
    """ Retrieves a User Object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """ Retrieves a User Object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return {}, 200


@app_views.route("/users", methods=["POST"])
def create_user():
    """ Create a new User object """
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400

    new_user = User(email=data["email"], password=data["password"])

    storage.new(new_user)
    storage.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """ Update a User object """
    one_user = storage.get(User, user_id)

    if not one_user:
        return jsonify({"error": "Not found"}), 404

    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(one_user, key, value)

    storage.save()
    return jsonify(one_user.to_dict()), 200

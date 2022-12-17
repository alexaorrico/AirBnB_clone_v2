#!/usr/bin/python3
"""Module for User endpoints"""
from flask import jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'],
                 defaults={"user_id": None})
@app_views.route('/users/<user_id>', methods=['GET'])
def get_users(user_id):
    """Retrieves the list of all User objects
    or a specific user"""
    if user_id is None:
        return jsonify([v.to_dict() for v in storage.all(User).values()])
    user = storage.get(User, user_id)
    if not user:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_users(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if not user:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def post_user():
    """POST /user API route"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in data:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in data:
        return make_response(jsonify({"error": "Missing password"}), 400)
    s = User(**data)
    s.save()
    return make_response(jsonify(s.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"])
def put_user(user_id):
    """PUT /user API route"""
    user = storage.get(User, user_id)
    if not user:
        return make_response(jsonify({"error": "Not found"}), 404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)

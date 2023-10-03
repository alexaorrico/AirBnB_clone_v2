#!/usr/bin/python3
"""View for User class"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.user import User
from flask import abort
from flask import make_response
from flask import request


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def all_users():
    """Return all users"""
    dic_users = storage.all(User)
    list_users = []
    for v in dic_users.values():
        list_users.append(v.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET'])
def get_user(user_id):
    """Return a user according class and id of a user"""
    if user_id:
        dic_users = storage.get(User, user_id)
        if dic_users is None:
            abort(404)
        else:
            return jsonify(dic_users.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """Delete a user if the id exists,if not, raise an error"""
    if user_id:
        users = storage.get(User, user_id)
        if users is None:
            abort(404)
        else:
            storage.delete(users)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def post_user():
    """Post  a user to the storage"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    reque = request.get_json()
    if "email" not in reque:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in reque:
        return make_response(jsonify({"error": "Missing password"}), 400)
    users = User(**reque)
    users.save()
    return make_response(jsonify(users.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    """Updates details of a user"""
    if user_id:
        users = storage.get(User, user_id)
        if users is None:
            abort(404)

        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        reque = request.get_json()
        for key, value in reque.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(users, key, value)
        users.save()
        return make_response(jsonify(users.to_dict()), 200)

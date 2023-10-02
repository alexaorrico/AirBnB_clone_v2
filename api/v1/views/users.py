#!/usr/bin/python3
"""
    states.py file in v1/views
"""
from flask import abort, Flask, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
def handle_users():
    """
        Method to return a JSON representation of all states
    """
    if request.method == 'GET':
        users = storage.all(User)
        all_users = []
        for user in users.values():
            all_users.append(user.to_dict())
        return jsonify(all_users)
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('email') is None:
            return jsonify({'error': 'Missing email'}), 400
        elif post.get('password') is None:
            return jsonify({'error': 'Missing password'}), 400
        new_user = User(**post)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def handle_user_by_id(user_id):
    """
        Method to return a JSON representation of a state
    """
    user_by_id = storage.get(User, user_id)
    if user_by_id is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(user_by_id.to_dict())
    elif request.method == 'DELETE':
        storage.delete(user_by_id)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'message': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user_by_id, key, value)
        storage.save()
        return jsonify(user_by_id.to_dict()), 200

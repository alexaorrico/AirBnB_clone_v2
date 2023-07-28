#!/usr/bin/python3
"""Creatte the states function"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
import models


@app_views.route('/users', methods=['GET'])
def get_all_users():
    """retrieves all users"""
    all_state = []
    for enu in models.storage.all("User").values():
        all_state.append(enu.to_dict())
    return jsonify(all_state)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_a_user_with_id(user_id):
    """get a user using id"""
    answer = models.storage.get("User", user_id)
    if answer:
        return jsonify(answer.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_a_user_with_id(user_id):
    """delete a state using id"""
    answer = models.storage.get("User", user_id)
    if answer:
        answer.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/users', methods=['POST'])
def add_a_user():
    """create a user"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.json:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.json:
        return jsonify({"error": "Missing password"}), 400
    values = request.get_json()
    new_state = User(**values)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_a_user_with_id(user_id):
    """update a user using id"""
    answer = models.storage.get("User", user_id)
    if answer:
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in request.get_json().items():
            if k not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(answer, k, v)
        answer.save()
        return jsonify(answer.to_dict()), 200
    abort(404)

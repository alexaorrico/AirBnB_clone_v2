#!/usr/bin/python3
"""
User Model
"""
import json
from flask import Flask, request, jsonify, abort
from models.user import User
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


@app_views.route('/users/', methods=['GET'])
def get_all_users():
    """
    Retrieves all users from the storage and returns them as a JSON response.
    """
    user_list = []
    user_dict = storage.all(User)
    for item in user_dict:
        user_list.append(user_dict[item].to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_one_users(user_id):
    """
    Retrieves a specific user from the storage and returns it as a JSON
    response.
    """
    users_dict = storage.all(User)
    for item in users_dict:
        if users_dict[item].to_dict()['id'] == user_id:
            return jsonify(users_dict[item].to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_one_users(user_id):
    """
    Deletes a specific user from the storage.
    """
    the_user = storage.get(User, user_id)
    if the_user is not None:
        storage.delete(the_user)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users/', methods=['POST'])
def post_user():
    """
    Creates a new user in the storage.
    """
    content = request.headers.get('Content-type')
    if content != 'application/json':
        abort(400, description='Not a JSON')
    json_dict = request.json
    if 'email' not in json_dict:
        abort(400, description='Missing email')
    if 'password' not in json_dict:
        abort(400, description='Missing password')
    new_user = User()
    for item in json_dict:
        setattr(new_user, item, json_dict[item])
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user_attribute(user_id):
    """
    Updates a specific user in the storage.
    """
    the_user = storage.get(User, user_id)
    if the_user is None:
        abort(404)
    content = request.headers.get('Content-type')
    if content != 'application/json':
        abort(400, description='Not a JSON')
    j = request.json
    for i in j:
        if i not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(the_user, i, j[i])
    storage.save()
    return jsonify(the_user.to_dict()), 200

#!/usr/bin/python3
"""User management endpoints"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from datetime import datetime
import uuid


@app_views.route('/users/', methods=['GET'])
@app_views.route('/users', methods=['GET'])
def list_users():
    '''Fetches all User objects'''
    users_list = [item.to_dict() for item in storage.all("User").values()]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    '''Fetches a specific User object by ID'''
    all_users = storage.all("User").values()
    user_data = [item.to_dict() for item in all_users if item.id == user_id]
    if not user_data:
        abort(404)
    return jsonify(user_data[0])


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    '''Deletes a specific User object by ID'''
    all_users = storage.all("User").values()
    user_data = [item.to_dict() for item in all_users if item.id == user_id]
    if not user_data:
        abort(404)
    user_data.remove(user_data[0])
    for item in all_users:
        if item.id == user_id:
            storage.delete(item)
            storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    '''Creates a new User object'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')
    users_collection = []
    new_user = User(email=request.json['email'], \
      password=request.json['password'])
    storage.new(new_user)
    storage.save()
    users_collection.append(new_user.to_dict())
    return jsonify(users_collection[0]), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    '''Updates a specific User object'''
    all_users = storage.all("User").values()
    user_data = [item.to_dict() for item in all_users if item.id == user_id]
    if not user_data:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    try:
        user_data[0]['first_name'] = request.json['first_name']
    except KeyError:
        pass
    try:
        user_data[0]['last_name'] = request.json['last_name']
    except KeyError:
        pass
    for item in all_users:
        if item.id == user_id:
            try:
                if request.json.get('first_name') is not None:
                    item.first_name = request.json['first_name']
            except KeyError:
                pass
            try:
                if request.json.get('last_name') is not None:
                    item.last_name = request.json['last_name']
            except KeyError:
                pass
    storage.save()
    return jsonify(user_data[0]), 200

#!/usr/bin/python3
"""Users"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from datetime import datetime
import uuid


@app_views.route('/api/v1/users/', methods=['GET'], strict_slashes=False)
def list_users():
    '''Retrieves a list of all users objects'''
    users_list = [obj.to_dict()
                  for obj in storage.all("User").values()]
    return jsonify(users_list)


@app_views.route('/api/v1/users/<user_id>', methods=['GET'])
def get_users(user_id):
    '''Retrieves an users object'''
    all_user = storage.all("User").values()
    u_obj = [obj.to_dict() for obj in all_user
             if obj.id == user_id]
    if u_obj == []:
        abort(404)
    return jsonify(u_obj[0])


@app_views.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    '''Deletes an users object'''
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users
                if obj.id == user_id]
    if user_obj == []:
        abort(404)
    user_obj.remove(user_obj[0])
    for obj in all_users:
        if obj.id == user_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/users', methods=['POST'])
def create_user():
    '''Creates an User'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    users = []
    new_user = User(name=request.json['name'])
    storage.new(new_user)
    storage.save()
    users.append(new_user.to_dict())
    return jsonify(users[0]), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updates_user(user_id):
    '''Updates an User object'''
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users
                if obj.id == user_id]
    if user_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    user_obj[0]['name'] = request.json['name']
    for obj in all_users:
        if obj.id == user_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(user_obj[0]), 200

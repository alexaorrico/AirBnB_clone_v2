#!/usr/bin/python3
'''
    RESTful API for class User
'''
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    '''
        return all user objects in json form
    '''
    user_list = [u.to_dict() for u in storage.all('User').values()]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    '''
        return user with given id using http verb GET
    '''
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    '''
        delete user obj given user_id
    '''
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''
        create new user obj
    '''
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "email" not in data:
        return make_response(jsonify({"error": "Missing email"}), 400)
    elif "password" not in data:
        return make_response(jsonify({"error": "Missing password"}), 400)
    else:
        obj = User(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''
        update existing user object
    '''
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    keys = ["id", "email", "created_at", "updated_at"]
    for key in data.keys():
        if key not in keys:
            setattr(obj, key, data[keys])
    obj.save()
    return jsonify(obj.to_dict()), 200

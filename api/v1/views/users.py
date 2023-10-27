#!/usr/bin/python3
'''
    RESTful API for class User
'''
from flask import Flask, jsonify, abort, request
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
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "email" not in request.get_json():
        return jsonify({"error": "Missing email"}), 400
    elif "password" not in request.get_json():
        return jsonify({"error": "Missing password"}), 400
    else:
        obj_data = request.get_json()
        obj = User(**obj_data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''
        update existing user object
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    obj_data = request.get_json()
    ignore = ("id", "email", "created_at", "updated_at")
    for k in obj_data.keys():
        if k in ignore:
            pass
        else:
            setattr(obj, k, obj_data[k])
    obj.save()
    return jsonify(obj.to_dict()), 200

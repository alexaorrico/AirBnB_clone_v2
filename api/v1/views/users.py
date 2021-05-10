#!/usr/bin/python3
"""new view for User object that handles all"""
from models.user import User
from models.amenity import Amenity
from flask import Flask, abort, jsonify, make_response
from flask import request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/users', methods=['GET'])
def all_users():
    """return all Users"""
    users = storage.all(User).values()
    list_users = []
    for user in users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'])
def user_id(user_id=None):
    """return users"""
    if user_id is not None:
        my_user_obj = storage.get(User, user_id)
        if my_user_obj is None:
            abort(404)
        else:
            return jsonify(my_user_obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def user_delete(user_id=None):
    """delete user"""
    if user_id is not None:
        my_user_obj = storage.get(User, user_id)
        if my_user_obj is None:
            abort(404)
        else:
            storage.delete(my_user_obj)
            return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'])
def user_post():
    """POST user"""
    my_json = request.get_json(silent=True)
    if my_json is not None:
        if "email" in my_json:
            if "password" in my_json:
                email = my_json["email"]
                password = my_json["password"]
                new_city = User(email=email, password="password")
                new_city.save()
                return make_response(jsonify(new_city.to_dict()), 201)
            else:
                abort(400, "Missing password")
        else:
            abort(400, "Missing email")
    else:
        abort(400, "Not a JSON")


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id=None):
    """PUT user"""
    if user_id is not None:
        my_user_obj = storage.get(User, user_id)
        if my_user_obj is None:
            abort(404)
        else:
            update_ = request.get_json(silent=True)
            if update_ is not None:
                for key, value in update_.items():
                    setattr(my_user_obj, key, value)
                    my_user_obj.save()
                return make_response(jsonify(my_user_obj.to_dict()), 200)
            else:
                abort(400, "Not a JSON")

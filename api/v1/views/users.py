#!/usr/bin/python3
"""view for User object that handles all defaut RESTFul API actions"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify
from flask import make_response
from flask import request
from flask import abort


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def getUsers():
    """retrieves the list of all User objects"""
    all_users = storage.all(User)
    user_list = [val.to_dict() for val in all_users.values()]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def getUser(user_id):
    """retrieve a User object"""
    all_users = storage.all(User)
    for val in all_users.values():
        if val.id == user_id:
            return jsonify(val.to_dict())
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def deleteUser(user_id):
    """delete a User object"""
    all_users = storage.all(User)
    for val in all_users.values():
        if val.id == user_id:
            storage.delete(val)
            storage.save()
            return make_response(jsonify({}), 200)
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def createUser():
    """create a User"""
    all_users = storage.all(User)
    try:
        data = request.get_json()
        if "email" not in data:
            return make_response("Missing email", 400)
        if "password" not in data:
            return make_response("Missing password", 400)
        new_user = User()
        for key, value in data.items():
            setattr(new_user, key, value)
        storage.new(new_user)
        storage.save()
        return make_response(jsonify(new_user.to_dict()), 201)
    except Exception as e:
        return make_response("Not a JSON", 400)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def updateUser(user_id):
    """update a User object"""
    all_users = storage.all()
    try:
        data = request.get_json()
        for val in all_users.values():
            if val.id == user_id:
                for k, v in data.items():
                    setattr(val, k, v)
                storage.save()
                return make_response(jsonify(val.to_dict()), 200)
        return make_response(jsonify({"error": "Not found"}), 404)
    except Exception as e:
        return make_response("Not a JSON", 400)

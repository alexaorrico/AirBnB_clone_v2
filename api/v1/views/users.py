#!/usr/bin/python3
"""
this module creates a new view for User objects
that handles all default RESTFul API actions
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def getUsers():
    """
    returns all users
    """
    usersInstances = storage.all(User).values()
    users = [user.to_dict() for user in usersInstances]
    return jsonify(users), 200


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def getUserById(user_id):
    """
    returns a user by its id
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def deletesUser(user_id):
    """
    deletes a user
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def postUser():
    """
    creates new user
    """
    if request.is_json:
        argsDict = request.args
        argsDict = request.get_json()
        if 'email' not in argsDict:
            return jsonify(message="Missing email"), 400
        if 'password' not in argsDict:
            return jsonify(massage="Missing password"), 400
        email = argsDict['email']
        password = argsDict['password']
        newUser = User(email=email, password=password)
        newUser.save()
        newUserDict = storage.get(User, newUser.id).to_dict()
        return jsonify(newUserDict), 201
    else:
        return jsonify(message="Not a JSON"), 400


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def updateUser(user_id):
    """
    updates a user
    """
    user = storage.get(User, user_id)
    if user:
        forbidden_keys = ['id', 'email', 'created_at', 'updated_at']
        if request.is_json:
            argsDict = request.args
            argsDict = request.get_json()
            for k, v in argsDict.items():
                if k not in forbidden_keys:
                    setattr(user, k, v)
            user.save()
            return jsonify(user.to_dict()), 200
        else:
            return jsonify(message="Not a JSON"), 400
    else:
        abort(404)

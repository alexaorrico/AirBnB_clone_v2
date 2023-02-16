#!/usr/bin/python3
"""create a new view for City objects that
   handles all default RESTFul API actions:
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def getAllUser():
    """ gets  all the users """
    UserList = []
    allUser = storage.all(User)
    for val in allUser.values():
        UserList.append(val.to_dict())
    return jsonify(UserList)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def getUser(user_id):
    """ Get a user by Id"""
    UserList = []
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def deleteUser(user_id):
    """ deletes a user given the id """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def postUser():
    """ adds a user"""
    PostDict = request.get_json()
    if not PostDict:
        abort(400, description="Not a JSON")
    if "email" not in PostDict:
        abort(400, description="Missing email")
    if "password" not in PostDict:
        abort(400, description="Missing password")
    UpdatedClass = User(**PostDict)
    UpdatedClass.save()
    return make_response(jsonify(UpdatedClass.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def PutUser(user_id):
    """updates the user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignoreList = ['id', 'email', 'created_at', 'updated_at']
    data = request.get_json()
    for k, v in data.items():
        if k not in ignoreList:
            setattr(user, k, v)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)

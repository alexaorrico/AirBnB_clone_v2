#!/usr/bin/python3
"""
module amenities.py
"""

from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def userObjects():
    """ Retrieves the list of all User objects """
    user = storage.all(User)
    userList = []
    for us in user.values():
        userDict = us.to_dict()
        userList.append(userDict)
    """states_list = [state.to_dict() for state in states.values()]"""
    return jsonify(userList)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def userObjectWithId(user_id):
    """Retrieves an User object with it's id"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def userDeleteWithId(user_id):
    """Deletes an User object"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def createUser():
    """Creates a User: POST /api/v1/users"""
    """same as 'if not request.is_json'"""
    if request.headers.get('Content-Type') != "application/json":
        abort(400, description="Not a JSON")

    newUserData = request.get_json()

    if not newUserData.get("email"):
        abort(400, description="Missing email")
    if not newUserData.get("password"):
        abort(400, description="Missing password")

    newUserObj = User(**newUserData)
    storage.new(newUserObj)
    storage.save()

    return jsonify(newUserObj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def updateUser(user_id):
    """Updates a User object: PUT /api/v1/amenities/<amenity_id>"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    userUpdateData = request.get_json()
    userObj = storage.get(User, user_id)
    if userObj:
        ignoredKeys = ['id', 'email', 'created_at', 'updated_at']
        for k, v in userUpdateData.items():
            if k not in ignoredKeys:
                setattr(userObj, k, v)
        storage.save()
        return jsonify(userObj.to_dict()), 200
    else:
        abort(404)

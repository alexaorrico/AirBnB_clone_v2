#!/usr/bin/python3
""" Create a new view for User object that handles all
    default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def allUsers():
    '''Retrieves the list of all Users objects of a State:
    GET /api/v1/states/<state_id>/amenities'''

    allUsers = storage.all(User)
    listUser = []
    for user in allUsers.values():
        listUser.append(user.to_dict())
    return jsonify(listUser)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def objUsers(user_id):
    '''Retrieves a User object. :
    GET /api/v1/users/<user_id>'''
    users = storage.get('User', user_id)
    if users:
        return jsonify(users.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteUser(user_id):
    '''Deletes a Amenities object:
    DELETE /api/v1/amenities/<amenity_id>'''
    UserI = storage.get('User', user_id)
    if UserI:
        storage.delete(UserI)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def createUser():
    '''Creates a User:
    POST /api/v1/states/<state_id>/user'''
    dataRequest = request.get_json()
    if dataRequest:
        if dataRequest.get('email') is None:
            abort(400, 'Missing email')
        if dataRequest.get('password') is None:
            abort(400, 'Missing password')
        newUser = User(**dataRequest)
        storage.new(newUser)
        storage.save()
        return jsonify(newUser.to_dict()), 201
    else:
        abort(400, "Not a JSON")


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def updateUser(user_id):
    '''Updates a User object:
    PUT /api/v1//users/<user_id>'''
    obj = storage.get('User', user_id)
    if obj:
        data_request = request.get_json()
        if isinstance(data_request, dict):
            noKeys = ['id', 'state_id', 'created_at', 'updated_at']
            for key, value in data_request.items():
                if key not in noKeys:
                    setattr(obj, key, value)
            obj.save()
            return jsonify(obj.to_dict()), 200
        else:
            abort(400, 'Not a JSON')
    else:
        abort(404)

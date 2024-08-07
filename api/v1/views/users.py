#!/usr/bin/python3
'''users blueprint'''

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=['GET'],
                 strict_slashes=False)
def getUserById(user_id=None):
    '''gets user by id'''
    if user_id is None:
        users = storage.all(User)
        return jsonify([user.to_dict() for user in users.values()])

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def deleteUser(user_id=None):
    '''deletes an user'''
    if user_id is not None:
        res = storage.get(User, user_id)
        if res is not None:
            storage.delete(res)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/users',
                 methods=['POST'],
                 strict_slashes=False)
def postUser():
    '''posts a new user'''
    body = request.get_json()
    if body is None or type(body)is not dict:
        abort(400, description='Not a JSON')
    if 'email' not in body.keys():
        abort(400, description='Missing email')
    if 'password' not in body.keys():
        abort(400, description='Missing password')

    user = User(**body)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def updateUser(user_id=None):
    '''updates a user'''
    if user_id is None:
        abort(404)
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400, description='Not a JSON')
    for key in body.keys():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(obj, key, body[key])
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)

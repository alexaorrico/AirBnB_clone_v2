#!/usr/bin/python3
'''
This module handles all default RESTFul API actions for the user object
this handle actions of creating, reading and updating and Deleting user objects
from the storage
'''
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET', 'POST'], strict_slashes=False)
def users():
    '''this function lists a all users from the database in the case of
    GET REQUESTS:
    POST  request, the post request must have
    email address, and password and must be in json '''
    if request.method == 'GET':
        user_objs = storage.all('User')
        return jsonify([obj.to_dict() for obj in user_objs.values()])

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if data.get("email") is None:
        abort(400, "Missing email")
    if data.get("password") is None:
        abort(400, "Missing password")
    user_obj = User(**data)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.route('/users/<user_id>/', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def get_user(user_id):
    '''theif gunction handles handles
    GET REQUESTS : this looks for a user if in database and display
    PUT REQUEST : this updates the user with matching ID in the database
    DELETE REQUEST: this deletes a request with matching id in the database
    user_id : this the id of the user to perform a request on'''
    user_objs = storage.all('User')
    key = 'User.{}'.format(user_id)

    if request.method == 'GET':
        if key in user_objs:
            user = user_objs.get(key)
            return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        if key in user_objs:
            obj = user_objs.get(key)
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    else:
        if key not in user_objs:
            abort(404)
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        user = user_objs.get(key)
        for k, v in data.items():
            setattr(user, k, v)
        user.save()
        return jsonify(user.to_dict()), 200
    abort(404)

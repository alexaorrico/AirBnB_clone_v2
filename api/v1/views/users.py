#!/usr/bin/python3
'''This module Retrieves the list of all City objects,
deletes, updates, creates and gets information of a city '''

from flask import jsonify, request, abort, make_response
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def get_all_users():
    ''' retreive all users '''
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
def get_an_user(user_id):
    '''return the user with matching id'''
    user_objs = storage.all('User')
    key = f'User.{user_id}'

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

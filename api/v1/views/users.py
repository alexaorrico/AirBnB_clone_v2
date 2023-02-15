#!/usr/bin/python3
"""
handles all RESTFUl API actions for Users
"""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.engine.db_storage import classes


@app_views.route('/users', methods=['GET', 'POST'])
def all_users():
    """ defines route for api/v1/users """
    if request.method == 'GET':
        user = [u.to_dict() for u in storage.all('User').values()]
        return jsonify(user)

    if request.method == 'POST':
        if not request.json:
            return make_response('Not a JSON', 400)
        if 'email' not in request.json:
            return make_response('Missing email', 400)
        if 'password' not in request.json:
            return make_response('Missing password', 400)
        newObj = classes['User']
        newUser = newObj(**request.json)
        newUser.save()
        return jsonify(newUser.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user_by_id(user_id):
    """ defines route for api/vi/users/<user_id> """
    allUser = [u for u in storage.all('User').values()]
    user = [u for u in allUser if u.id == user_id]
    if request.method == 'GET':
        if (len(user) == 0):
            abort(404)
        return jsonify(user[0].to_dict())

    if request.method == 'DELETE':
        if len(user) == 0:
            return make_response('Not found', 404)
        storage.delete(user[0])
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        if len(user) == 0:
            abort(404)
        if not request.json:
            return make_response('Not a JSON', 400)
        data = request.json
        for key, value in data.items():
            if key not in ['id', 'email', 'created_at', 'updated_ap']:
                setattr(user[0], key, value)
                user[0].save()
        return jsonify(user[0].to_dict()), 200

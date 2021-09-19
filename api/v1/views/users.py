#!/usr/bin/python3
""" handles all default RESTFul API actions """
from os import abort, stat
from flask import json
from sqlalchemy.sql.sqltypes import String
from models.user import User
from flask.json import jsonify
from api.v1.views import app_views
from flask import request, abort

@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def get_all_users():
    """ manipulate on User model """
    from models import storage
    # get the list of all users in database
    if request.method == "GET":
        users = storage.all('User')
        l = []
        for user in users.values():
            l.append(user.to_json())
        return(jsonify(l))
    # add new user to the database
    if request.method == "POST":
        # transform body request to dictionary
        json_req = request.get_json()
        if json_req is None:
            abort(400, 'Not a JSON')
        if json_req.get("email") is None:
            abort(400, 'Missing email')
        if json_req.get("password") is None:
            abort(400, 'Missing password')
        new_user = User(**json_req)
        new_user.save()
        return jsonify(new_user.to_json()), 201

@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET', 'POST', 'DELETE', 'PUT'])
def handle_users_with_id(user_id=None):
    """ User manipulation based on user_id """
    from models import storage
    user = storage.get('User', user_id)
    if user is None:
        abort(404, 'Not Found')
    if request.method == "GET":
        return jsonify(user.to_json())
    if request.method == "DELETE":
        # delete user corresponding to user_id
        user.delete()
        storage.save()
        return jsonify({})
    if request.method == "PUT":
        # modify the user with corresponding user_id
        json_req = request.get_json()
        if json_req is None:
            abort(400, 'Not a JSON')
        user.update(json_req)
        return jsonify(user.to_json()), 200
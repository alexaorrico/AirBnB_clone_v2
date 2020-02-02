#!/usr/bin/python3
""" Create a new view for User that handles all default RestFul API """

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import Flask, jsonify, abort, request


@app_views.route('/users/',  methods=['GET'], strict_slashes=False)
def Users_Get():
    """ Retrieve all the users"""

    data = storage.all('User')
    var = []

    for value in data.values():
        var.append(value.to_dict())

    return jsonify(var)


@app_views.route('/users/<user_id>',  methods=['GET'], strict_slashes=False)
def Users_Id(user_id):
    """ Retrieve an user by id """
    data = storage.all('User')
    for key, value in data.items():
        key = key.split(".")
        if key[-1] == user_id:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def User_Delete(user_id):
    """ Retrieve an user by id """
    data = storage.all('User')
    del_user = storage.get('User', user_id)
    if del_user is None:
        abort(404)
    storage.delete(del_user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def Users_Post():
    """ Post """

    data = request.get_json()

    if not data:
        return jsonify({"message": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"message": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"message": "Missing password"}), 400

    # name_user = {"name": data["name"]}
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def User_Put(user_id):
    """ Put """
    data = storage.get('User', user_id)
    data_req = request.get_json()

    if data is None:
        abort(404)
    if not data_req:
        return jsonify({"message": "Not a JSON"}), 400

    for key, value in data_req.items():
        if key in ['id', 'email', 'created_at', 'updated_at']:
            continue
        setattr(data, key, value)
    data.save()
    return jsonify(data.to_dict()), 200
    
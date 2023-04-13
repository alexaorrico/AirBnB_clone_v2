#!/usr/bin/python3
"""First route to display a json object"""
from models.user import User
from flask import jsonify, request
from models import storage
from api.v1.views import app_views


@app_views.route('/users/', methods=['GET', 'POST'],
                 defaults={'user_id': None})
@app_views.route('/users/<user_id>',
                 methods=['GET', 'POST', 'DELETE', 'PUT'])
def users_views(user_id=None):
    if user_id is not None:
        my_user = storage.get(User, user_id)
        if my_user is None:
            return jsonify(error='Amenity not found'), 404
        if request.method == 'GET':
            return jsonify(my_user.to_dict())
        if request.method == 'DELETE':
            storage.delete(my_user)
            storage.save()
            return {}, 200
        if request.method == 'PUT':
            update_values = request.get_json()
            if type(update_values) is not dict:
                return jsonify(error='Not a JSON'), 400
            for key, val in update_values.items():
                ls = ['id', 'created_at', 'updated_at', 'email']
                if key not in ls:
                    setattr(my_user, key, val)
                storage.save()
                return jsonify(my_user.to_dict())
    else:
        if request.method == 'GET':
            curr = storage.all(User)
            new_user_list = []
            print(type(new_user_list))
            for user in curr.values():
                new_user_list.append(user.to_dict())
            return jsonify(new_user_list)
        if request.method == 'POST':
            new_object = request.get_json()
            if type(new_object) is not dict:
                return jsonify(error='Not a JSON'), 400
            if 'email' not in new_object.keys():
                return jsonify(error='Missing email'), 400
            if 'password' not in new_object.keys():
                return jsonify(error='Missing password'), 400
            new_user = User(**new_object)
            storage.new(new_user)
            storage.save()
            return jsonify(new_user.to_dict()), 201

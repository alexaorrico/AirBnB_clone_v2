#!/usr/bin/python3
"""
Module for users objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', defaults={'user_id': None}, methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """ Retrieves the list of all User objects """
    if user_id is None:
        amenities_list = []
        for value in storage.all(User).values():
            amenities_list.append(value.to_dict())
        return jsonify(amenities_list)
    else:
        try:
            user_dic = storage.get(User, user_id).to_dict()
            return jsonify(user_dic)
        except:
            abort(404)


@app_views.route('/users', methods=['POST'])
def create_user():
    """ Create a new User object """
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'email' not in request.json:
        return make_response(jsonify({"error": "Missing email"}), 400)

    if 'password' not in request.json:
        return make_response(jsonify({"error": "Missing password"}), 400)

    data = request.get_json()
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ Update a User object """
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    try:
        user_obj = storage.get(User, user_id)
        data = request.get_json()

        for key, value in data.items():
            if (key != 'id' or key != 'email'
               or key != 'created_at' or key != 'updated_at'):
                setattr(user_obj, key, value)

        storage.save()
        return jsonify(user_obj.to_dict()), 200
    except:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Delete a User object """
    user_obj = storage.get(User, user_id)
    if user_obj is not None:
        storage.delete(user_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

#!/usr/bin/python3
"""
Users file
"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def jsonify_users_1():
    """ Function that returns a JSON """
    the_obj = storage.all(User)
    my_list = []
    for obj in the_obj.values():
        my_list.append(obj.to_dict())
    return jsonify(my_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def jsonify_users_2(user_id):
    """ Function that returns a JSON"""
    the_obj = storage.get(User, user_id)
    if the_obj is None:
        abort(404)
    return jsonify(the_obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def jsonify_users_3(user_id):
    """ Function delete a User Object """
    the_obj = storage.get(User, user_id)
    if the_obj is None:
        abort(404)
    storage.delete(the_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def jsonify_users_4():
    """ Creates a User object """
    json_post = request.get_json()
    if not json_post:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in json_post:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in json_post:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    new = User(**json_post)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def jsonify_users_5(user_id):
    """ Update a User object """
    the_obj = storage.get(User, user_id)
    json_put = request.get_json()
    if the_obj is None:
        abort(404)
    if not json_put:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in json_put.items():
        if key not in ['id', 'email', 'created_at', 'update_at']:
            setattr(the_obj, key, value)
    storage.save()
    return make_response(jsonify(the_obj.to_dict()), 200)

#!/usr/bin/python3
'''
Handles all default RESTFul API actions for User objects
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User

F = False


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user_objs():
    '''handles Get for all users objects'''

    user_list = []
    objs = storage.all()
    for k, v in objs.items():
        if v.__class__.__name__ == "User":
            user_list.append(v.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=F)
def get_user_obj(user_id):
    '''handles Get for a user object'''

    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)

    user_dict = user_obj.to_dict()
    return jsonify(user_dict)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=F)
def delete_user_obj(user_id):
    '''deletes a user object'''

    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)

    storage.delete(user_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user_obj():
    '''creates users objects'''

    json_data = request.get_json()
    if json_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'email' not in json_data.keys():
        return jsonify({"error": "Missing email"}), 400
    elif 'password' not in json_data.keys():
        return jsonify({"error": "Missing password"}), 400

    new_obj = User()
    for attr, val in json_data.items():
        setattr(new_obj, attr, val)
    # new_obj = State(**json_data)
    new_obj.save()

    return jsonify(new_obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=F)
def update_user_objs(user_id):
    '''updates a user object'''

    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for attr, val in json_data.items():
        if attr not in ("id", "email", "created_at", "updated_at"):
            setattr(user_obj, attr, val)
    user_obj.save()

    return jsonify(user_obj.to_dict()), 200

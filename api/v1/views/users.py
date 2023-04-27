#!/usr/bin/python3
'''
Create a new view for User objects that handles all default HTTP methods
'''
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_user():
    """  list of all Users objects """

    all_user = storage.all(User).values()
    all_users = [user.to_dict() for user in all_user]

    return jsonify(all_users)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user_by_name(user_id=None):
    """ display a resource of my list of users """

    user_object = storage.get(User, user_id)
    if user_object is None:
        abort(404)
    return jsonify(user_object.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id=None):
    """ delete a resource of my list of users """

    delete_user = storage.get(User, user_id)
    if delete_user is None:
        abort(404)
    else:
        storage.delete(delete_user)
        storage.save()
        return (jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_new_user(state_id=None):
    """ create new resource by my list of users """

    user_object_json = request.get_json()
    if user_object_json is None:
        return jsonify({'Error': 'Not a JSON'}), 400

    if 'email' not in user_object_json:
        return jsonify({'Error': 'Missing email'}), 400

    if 'password' not in user_object_json.keys():
        return jsonify({'Error': 'Missing password'}), 400

    user_object = User(**user_object_json)
    user_object.save()

    return jsonify(user_object.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_a_user(user_id=None):
    """ update a resource of my objects """

    user_object_json = request.get_json()
    if user_object_json is None:
        return jsonify({'Error': 'Not a JSON'}), 400

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    ignore = ['id', 'email', 'created_at', 'updated_at']

    for key, value in user_object_json.items():
        if key not in ignore:
            setattr(user, key, value)
    user.save()

    return jsonify(user.to_dict()), 200

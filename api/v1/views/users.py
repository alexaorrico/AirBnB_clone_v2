#!/usr/bin/python3

"""
A view designed for User instances, responsible for managing all
default RESTful API operations.

Author:
Khotso Selading and Londeka Dlamini
"""


from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, make_response, request


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def users():
    """retrieves of a list of all user objects"""
    return jsonify([obj.to_dict() for obj in storage.all('User').values()])


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET'])
def get_user(user_id):
    """retrieves specific user obj"""
    user_object = storage.get(User, user_id)

    if not user_object:
        abort(404)

    return jsonify(user_object.to_dict())


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_user(user_id):
    """deletes specific state object"""
    user_object = storage.get(User, user_id)

    if not user_object:
        abort(404)

    user_object.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def post_user():
    """adds new state object to filestorage/database"""
    new_user_object = request.get_json()

    if not new_user_object:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if new_user_object.get('email') is None:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if new_user_object.get('password') is None:
        return make_response(jsonify({"error": "Missing password"}), 400)

    user = User(**new_user_object)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def put_user(user_id):
    """adds new state object to filestorage/database"""
    user_object = storage.get(User, user_id)

    if not user_object:
        abort(404)
    new_user_object = request.get_json()
    if new_user_object is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in new_user_object.items():
        if key not in {'id', 'created_at', 'updated_at'}:
            setattr(user_object, key, value)

    user_object.save()
    return make_response(jsonify(user_object.to_dict()), 200)

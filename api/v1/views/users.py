#!/usr/bin/python3

"""
a view for User objects that handles all default RESTFul API actions

Authors: Khotso Selading and Londeka Dlamini
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
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_user(user_id):
    """deletes specific state object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def post_user():
    """adds new state object to filestorage/database"""
    json_body = request.get_json()
    if json_body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if json_body.get('email') is None:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if json_body.get('password') is None:
        return make_response(jsonify({"error": "Missing password"}), 400)
    user = User(**json_body)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def put_user(user_id):
    """adds new state object to filestorage/database"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    json_body = request.get_json()
    if json_body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in json_body.items():
        if key not in {'id', 'created_at', 'updated_at'}:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)

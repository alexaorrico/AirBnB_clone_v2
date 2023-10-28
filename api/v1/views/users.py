#!/usr/bin/python3
'''
    this script for RESTful API actions for user object
'''
from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    '''
        Retrieve all user objects
    '''
    user_list = []
    users = storage.all('User').values()
    for us in users:
        user_list.append = (us.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    '''
        Retrieve one user object
    '''
    try:
        city = storage.get('User', user_id)
        return jsonify(user.to_dict())
    except Exception:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    '''
        Delete a User object
    '''
    try:
        user = storage.get('User', user_id)
        storate.delete(user)
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    '''
        Create a user object
    '''
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.json:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.json:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(email=request.get_json(["email"]),
                    password=request.get_json(["password"]))
    for key, value in request.get_json.items():
        setattr(new_user, key, value)
    new_user.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id=None):
    '''
        Update a user object
    '''
    obj_users = storage.get('User', user_id)
    if obj_user is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.getjson():
        if key not in ['id', 'created_at', 'email', 'updated_at']:
            setattr(obj_user, key, value)
    obj_user.save()
    return (jsonify(obj_user.to_dict()), 200)

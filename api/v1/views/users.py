#!/usr/bin/python3

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    '''gets list of all users objects'''
    my_list = []
    for ob in storage.all(User).values():
        my_list.append(ob.to_dict())
    return jsonify(my_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    '''gets specific user object'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    '''deletes an user'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    '''Creates a new user'''
    j_dict = request.get_json()
    if not j_dict:
        return make_response({"error": "Not a JSON"}, 400)
    if 'name' not in j_dict:
        return make_response({"error": "Missing name"}, 400)
    user = User(**j_dict)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_User(user_id):
    '''update user object'''
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)

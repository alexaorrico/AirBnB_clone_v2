#!/usr/bin/python3
""" A new view that handles all default api actions on the users  """
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False,
                 methods=['GET'])
def lst_users():
    """ A route on the endpoint that returns a users list """
    all_users = storage.all(User).values()
    users_obj = [obj.to_dict() for obj in all_users]
    return jsonify(users_obj), 200


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET'])
def get_user(user_id):
    """ A route on the endpoint that returns a user """
    all_users = storage.all(User).values()
    users_obj = [obj.to_dict() for obj in all_users if
                 obj.id == user_id]
    if users_obj == []:
        abort(404)
    return jsonify(users_obj), 200


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """ A route that deletes a user based on the user id"""
    all_users = storage.all(User).values()
    users_obj = [obj.to_dict() for obj in all_users if
                 obj.id == user_id]
    if users_obj == []:
        abort(404)
    users_obj.remove(users_obj[0])
    for obj in all_users:
        if obj.id == user_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/users', strict_slashes=False,
                 methods=['POST'])
def post_user_objects():
    """ A route that allows addition of users to the storage"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')
    users = []
    new = User(name=request.json['name'], email=request.json['email'],
               password=request.get['password'])
    storage.new(new)
    storage.save()
    users.append(new.to_dict())
    return jsonify(users[0]), 201


@app_views.route('/users/user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    """ A route to update a specific user based on the user id"""
    all_users = storage.all(User).values()
    users_obj = [obj.to_dict() for obj in all_users if
                 obj.id == user_id]
    if user_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    users_obj[0]['name'] = request.json['name']
    for obj in all_users:
        if obj.id == user_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(userd_obj[0]), 200

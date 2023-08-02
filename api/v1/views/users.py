#!/usr/bin/python3
""" Flask views for the Amenities resource """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """ An endpoint that returns all users """
    rlist = []
    users = storage.all('User')
    for user in users.values():
        rlist.append(user.to_dict())
    return jsonify(rlist)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """ An endpoint that returns a specific user """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    else:
        return(jsonify(user.to_dict()))


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """ An endpoint that deletes a specific user """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', strict_slashes=False,
                 methods=['POST'])
def create_user():
    """ An endpoint that creates a new user """
    req_fields = ['email', 'password']
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    for field in req_fields:
        if field not in content:
            abort(400, 'Missing {}'.format(field))
    user = User(**content)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def modify_user(user_id):
    """ An endpoint that modifies an existing user """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    for k, v in content.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200

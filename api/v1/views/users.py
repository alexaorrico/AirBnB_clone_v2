#!/usr/bin/python3
""" User objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def allUsers():
    '''Retrieves the list of all Users objects of a State:
    GET /api/v1/states/<state_id>/amenities'''

    allUsers = storage.all(User)
    listUser = []
    for user in allUsers.values():
        listUser.append(user.to_dict())
    return jsonify(listUser)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def objUsers(user_id):
    '''Retrieves a User object. :
    GET /api/v1/users/<users_id>'''
    users = storage.get('User', user_id)
    if users:
        return jsonify(users.to_dict())
    else:
        abort(404)

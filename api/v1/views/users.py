#!/usr/bin/python3
""" Amenity objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
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

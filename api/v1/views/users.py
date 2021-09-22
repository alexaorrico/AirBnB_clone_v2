#!/usr/bin/python3
""" Handle RESTful API request for states"""

from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/users',
                 methods=['GET'],
                 strict_slashes=False)
def all_users():
    """ GET ALL USERS """

    objs = storage.all(User).values()
    list_obj = []
    for obj in objs:
        list_obj.append(obj.to_dict())

    return jsonify(list_obj)


@app_views.route('/users/<user_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_users(user_id):
    """ Retrieves a specific State """
    instance = storage.get(User, user_id)
    if not instance:
        abort(404)

    return jsonify(instance.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """delete a user"""
    obj = storage.get(User, user_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users',
                 methods=['POST'],
                 strict_slashes=False)
def create_users():
    """Creates a amenity """
    # validate data tyoe request
    if not request.get_json():
        abort(400, description="Not a JSON")
    # loads data request to a dict
    data = request.get_json()

    # validate minimal parameters to create a instance
    if 'name' not in data:
        abort(400, description="Missing name")
    if 'email'not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")

    # create a new_instance of the class
    new_instance = User(**data)
    new_instance.save()

    return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """update a State: POST /api/v1/states"""

    # validate data type request
    if not request.get_json():
        abort(400, description="Not a JSON")

    # validate if user_id exists
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)

    # loads request to dict
    data = request.get_json()

    # fields that have not update
    ignore = ['id', 'created_at', 'updated_at']

    # update attributes in object
    for key, value in data.items():
        if key not in ignore:
            setattr(obj, key, value)

    # saves object
    obj.save()

    return make_response(jsonify(obj.to_dict()), 200)

#!/usr/bin/python3
"""User module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User
from flasgger.utils import swag_from


# GET
@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get.yml', methods=['GET'])
def get_users():
    """Retrieve all User objects"""
    all_users = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(all_users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/user/get_id.yml', methods=['GET'])
def get_user(user_id):
    """Retrieve User by id"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    return jsonify(user.to_dict())


# DELETE
@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/user/delete.yml', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object by id"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    user.delete()
    storage.save()
    return jsonify({})


# POST
@app_views.route('/users/', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/user/post.yml', methods=['POST'])
def create_user():
    """ Creates User object"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)

    if 'password' not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)

    json_obj = request.get_json()
    obj = User(**json_obj)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


# PUT
@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/user/put.yml', methods=['PUT'])
def update_user(user_id):
    """Updates User object"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get(User, user_id)

    if obj is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated']:
            setattr(obj, key, value)

    storage.save()
    return jsonify(obj.to_dict())

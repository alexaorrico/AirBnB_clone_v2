#!/usr/bin/python3
"""View for user objects that handles all default RestFul API actions:"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def get_users():
    """ Retrieves the list of all user objects:
        GET /api/v1/users
    """
    users = []
    all_users = storage.all(user).values()

    for each in all_users:
        users.append(each.to_dict())

    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_users_by_id(user_id):
    """ Retrieves a user object:
        GET /api/v1/users/<user_id>
    """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a user object:
        DELETE /api/v1/users/<user_id>
    """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    user.delete()
    storage.save()

    return jsonify({})


@app_views.route('/users',
                 strict_slashes=False,
                 methods=['POST'])
def create_user():
    """ Creates a user:
        POST /api/v1/users
    """
    req_json = request.get_json()

    if not req_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "email" not in req_json:
        return make_response(jsonify({"error": "Missing email"}), 400)

    if "password" not in req_json:
        return make_response(jsonify({"error": "Missing password"}), 400)

    user = User(**req_json)
    user.save()

    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Updates a user object:
        PUT /api/v1/users/<user_id>
    """
    update_obj = storage.get(User, user_id)
    req_json = request.get_json()

    if not req_json:
        return jsonify({'error': 'Not a JSON'}), 400
    if obj:
        for key, value in req_json.items():
            setattr(update_obj, key, value)
        user.save()

        return jsonify(obj.to_dict()), 200
    else:
        abort(404)

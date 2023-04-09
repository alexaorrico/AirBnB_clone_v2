#!/usr/bin/python3

from flask import abort, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'])
def users_list():
    """returns all users"""

    from models import storage
    from models.user import User

    user_found = storage.all(User)
    if user_found == None:
        abort(404)

    user_list = []

    for user in user_found:
        user_list.append(user.to_dict())

    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def users(user_id):
    """returns user of id given"""

    from models import storage
    from models.user import User

    user_found = storage.get(User, user_id)
    if user_found == None:
        abort(404)

    return jsonify(user_found.to_dict())


@app_views.route('/users', methods=['POST'])
def create_user():
    """create an user"""
    from flask import request
    from models.user import User

    http_request = request.get_json(silent=True)
    if http_request == None:
        return 'Not a JSON', 400
    elif 'email' not in http_request.keys():
        return 'Missing email', 400
    elif 'password' not in http_request.keys():
        return 'Missing password', 400

    new_user = User(**http_request)
    storage.new(new_user)
    storage.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    """updates given user"""

    from flask import request
    from models.amenity import Amenity

    found_user = storage.get(Amenity, user_id)

    if found_user == None:
        return '', 404

    http_request = request.get_json(silent=True)
    if http_request == None:
        return 'Not a JSON', 400

    for key, values in http_request.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(found_user, key, values)

    storage.save()
    return jsonify(found_user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'])
def user_delete(user_id):
    """DELETE user if id is found"""

    from models import storage
    from models.user import User

    user_found = storage.get(User, user_id)
    if user_found == None:
        return '{}', 404

    storage.delete(user_found)
    storage.save()
    return jsonify({}), 200

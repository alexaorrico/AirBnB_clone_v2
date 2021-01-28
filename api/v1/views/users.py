#!/usr/bin/python3
"""New Funtion amenities"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    list_dict = []
    for obj in storage.all(User).values():
        list_dict.append(obj.to_dict())
    return make_response(jsonify(list_dict), 200)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieves a User object"""
    obj = storage.get(User, user_id)
    if (obj):
        return make_response(jsonify(obj.to_dict()), 200)
    else:
        abort(404)


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """Deletes a User object"""
    obj = storage.get(User, user_id)
    if (obj):
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user_create():
    """Creates a User"""
    conten = request.get_json()
    if conten is None:
        return make_response("Not a JSON", 400)
    if conten.get('email') is None:
        return make_response("Missing email", 400)
    elif conten.get('password') is None:
        return make_response("Missing password", 400)
    else:
        new_obj = User(**conten)
        storage.new(new_obj)
        storage.save()
    return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Updates a User object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, attr, val)
    storage.save()
    return jsonify(user.to_dict())

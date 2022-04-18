#!/usr/bin/python3
"""New view for User object that handles all default RestfulApi actions"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users_objs():
    """Return all Users"""
    return jsonify([obj.to_dict() for obj in storage.all(User).values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_by_id(user_id=None):
    """Return user by id"""
    user_objs = storage.get(User, user_id)
    if user_objs:
        return jsonify(user_objs.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    """Deletes a user object"""
    user_objs = storage.get(User, user_id)
    if user_objs:
        storage.delete(user_objs)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    """Create User object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    elif 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)

    dict_body = request.get_json()
    new_user = User(**dict_body)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_put(user_id=None):
    """Update user object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    dict_body = request.get_json()
    user_objs = storage.get(User, user_id)
    if user_objs:
        for key, value in dict_body.items():
            if key != "id" and key != "created_at" and key != "updated_at"\
                    and key != "email":
                setattr(user_objs, key, value)
        storage.save()
        return make_response(jsonify(user_objs.to_dict()), 200)
    else:
        return abort(404)

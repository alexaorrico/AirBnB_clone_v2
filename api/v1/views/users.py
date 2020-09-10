#!/usr/bin/python3
""" Restful API for User objects. """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ Retrieves a list with all users. """
    user_objs = storage.all(User).values()
    list_dic_users = []
    for user in user_objs:
        list_dic_users.append(user.to_dict())
    return jsonify(list_dic_users)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def new_user():
    """ Retrieves a new created user """
    body_dic = request.get_json()
    if not body_dic:
        return jsonify({'error': 'Not a JSON'}), 400
    if "email" not in body_dic:
        return jsonify({'error': 'Missing email'}), 400
    if "password" not in body_dic:
        return jsonify({'error': 'Missing password'}), 400
    new_user = User(**body_dic)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a current user"""
    user_obj = storage.get(User, user_id)
    if user_obj:
        body_dic = request.get_json()
        if not body_dic:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in body_dic.items():
            ignore_keys = ['id', 'created_at', 'email']
            if key not in ignore_keys:
                setattr(user_obj, key, value)
        user_obj.save()
        return jsonify(user_obj.to_dict()), 200
    else:
        abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete current user """
    user_obj = storage.get(User, user_id)
    if user_obj:
        storage.delete(user_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Get current user """
    user_obj = storage.get(User, user_id)
    if user_obj:
        return jsonify(user_obj.to_dict())
    else:
        abort(404)

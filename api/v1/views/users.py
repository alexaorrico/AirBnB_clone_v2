#!/usr/bin/python3
""" user objects """
from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """Create a new view for User objects that handles all default
    RestFul API actions.
    """
    if request.method == 'GET':
        return jsonify([val.to_dict() for val in storage.all('User')
                        .values()])
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('email') is None:
            return jsonify({'error': 'Missing email'}), 400
        elif post.get('password') is None:
            return jsonify({'error': 'Missing password'}), 400
        new_user = User(**post)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:user_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def get_user_id(user_id):
    """Retrieves a user object with a specific id"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        user = storage.get('User', user_id)
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)
                storage.save()
        return jsonify(user.to_dict()), 200

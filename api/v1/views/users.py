#!/usr/bin/python3

from flask import request, abort, jsonify
from api.v1.views import app_views
from models import storage, User


@app_views.route('/api/v1/users',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_users():

    if request.method == 'GET':
        return jsonify([value.to_dict()
                        for value in storage.all('User').values()])
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('email') is None:
            return jsonify({'error': 'Missing email'})
        elif post.get('password') is None:
            return jsonify({'error': 'Missing password'}), 400
        new_user = User(**post)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/api/v1/users/<string:user_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_user_id(user_id):
    """Retrieves the list of the User objects"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    elif request.method == 'PUT':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'})
        for key, value in post.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)
                storage.save()
                return jsonify(user.to_dict()), 200

    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

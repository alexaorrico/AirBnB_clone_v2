#!/usr/bin/python3
"""
This module handles the RESTful API actions for User objects
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_all_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])

@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a User object by user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.get('to_dict'()))

@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """deletes a User object by its id"""
    delete_response = REST_actions.delete(User, user_id)
    if delete_response.get('status code') == 404:
        abort(404)
    return jsonify({}),200

@app_views.route('/users', methods=['POST'])
def post_user():
    """creates a User"""
    request_body = request.get_json()
    if not request_body:
        return jsonify({'error': 'Not a JSON'}), 400
    if not request_body.get('email'):
        return jsonify({'error': 'Missing email'}), 400
    if not request_body.get('password'):
        return jsonify({'error': 'Missing password'}), 400
    new_user = User(**request_body)
    post_response = REST_actions.post(new_user)
    return post_response.get('object dict'), post_response.get('status code'), 201

app_views.route('/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    """ updates a User object by its id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    # Update User object with valid key-value pairs
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()
    return put_response.get('object dict'), put_response.get('status code')

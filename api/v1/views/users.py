#!/usr/bin/python3
"""
Creates API endpoints for acessing, creating,  deleting and
updating Users, it uses the app_views blueprint
"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, request, abort


@app_views.route('/users', methods=['GET'])
def get_users():
    """
    Retrieves all user objects and returns the JSON
    representation of the dictionary
    """
    users = []
    all_users = storage.all(User)

    for user in all_users.values():
        users.append(user.to_dict())
    return (jsonify(users))


@app_views.route('/users/<user_id>', methods=['GET'])
def get_a_user(user_id):
    """
    Retrieves a specific User based on their id
    404 error if the user does not exist
    """
    user = storage.get(User, user_id)

    if user is not None:
        return (jsonify(user.to_dict())), 200
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user  based on their id
    Returns an empty dictionary plus 200ok status on success
    or 404 error page on failure
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()

    return (jsonify({})), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """
    Creates a user and returns the dictionary representation of the
    user, or an error dictionary
    """
    data = request.get_json()
    if not data:
        return (jsonify({'error': 'Not a JSON'}))
    if 'email' not in data.keys():
        return (jsonify({'error': 'Missing email'}))
    if 'password' not in data.keys():
        return (jsonify({'error': 'Missing password'}))

    email = data.get('email')
    password = data.get('password')
    user = User(email=email, password=password)
    storage.new(user)
    storage.save()
    return (jsonify(user.to_dict())), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates a user based on the id, returns a code 201
    on success or an error dictionary
    """
    data = request.get_json()

    if not isinstance(data, dict):
        return (jsonify({'error': 'Not a JSON'}))

    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    exclude = ['id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in exclude:
            setattr(user, k, v)

    user.save()
    return (jsonify(user.to_dict())), 200

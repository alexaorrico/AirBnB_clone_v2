#!/usr/bin/python3
'''Create a new view for User objects - handles default RESTful API actions'''

from flask import abort, jsonify, request
# Import the User model
from models.user import User
from api.v1.views import app_views
from models import storage


# Route for retrieving all User objects
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    '''retrieves the list of all User objects'''
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


# Route that retrieves a specific User object by ID
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    '''Retrieves a User object'''
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


# Route for deleting a specific User object by ID
@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    '''Deletes a User object'''
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''Creates a User object'''
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


# Route for updating existing User object
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''Updates a User object'''
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)

        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    '''Returns 404: Not Found'''
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''Return Bad Request message for illegal requests to the API'''
    response = {'error': 'Bad Request'}
    return jsonify(response), 400

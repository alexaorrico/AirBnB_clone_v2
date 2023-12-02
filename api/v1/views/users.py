#!/usr/bin/python3
"""
Creating a new view for User objects - handling all default RESTful API actions
"""

from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views
from models import storage


# Retrieving all User objects
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def getting_all_users():
    '''
    Retrieves the list of all User objects.

    Returns:
    JSON: A list of dictionaries representing User objects.
    '''
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


# Retrieving a specific User object by ID
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def getting_user(user_id):
    '''
    Retrieves a User object.

    Args:
        user_id (str): The ID of the User.

    Returns:
        JSON: A dictionary representing the User object.

    Raises:
        404: If the User object is not found.
    '''
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


# Deleting a specific User object by ID
@app_views.route('/users/<user_id>', methods=['DELETE'])
def deleting_user(user_id):
    '''
    Deletes a User object.

    Args:
        user_id (str): The ID of the User.

    Returns:
        JSON: An empty dictionary.

    Raises:
        404: If the User object is not found.
    '''
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


# Creating a new User object
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def creating_user():
    '''
    Creates a User object.

    Returns:
        JSON: A dictionary representing the newly created User object.

    Raises:
        400: If the request data is not in JSON format
        or 'email'/'password' keys are missing.
    '''
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'email' not in data or 'password' not in data:
        abort(400, 'Missing email or password')

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


# Updating an existing User object by ID
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def updating_user(user_id):
    '''
    Updates a User object.

    Args:
        user_id (str): The ID of the User.

    Returns:
        JSON: A dictionary representing the updated User object.

    Raises:
        404: If the User object is not found.
        400: If the request data is not in JSON format.
    '''
    user = storage.get(User, user_id)
    if user and request.get_json():
        data = request.get_json()
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)

        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404 if not user else 400)

# Error Handlers:


@app_views.errorhandler(404)
def not_found(error):
    '''
    Returns 404: Not Found.

    Returns:
        JSON: A dictionary with the 'error' key set to 'Not found'.
    '''
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''
    Returns a Bad Request message for illegal requests to the API.

    Returns:
        JSON: A dictionary with the 'error' key set to 'Bad Request'.
    '''
    response = {'error': 'Bad Request'}
    return jsonify(response), 400

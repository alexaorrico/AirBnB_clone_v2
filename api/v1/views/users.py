#!/usr/bin/python3
"""
Flask Blueprint for user
"""

# Import necessary libraries and modules
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


# Define a route to retrieve all User objects
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""

    # Retrieve all User objects from the storage
    users = storage.all(User)

    # Return a JSON response containing a list of User objects
    return jsonify([user.to_dict() for user in users.values()])


# Define a route to retrieve a specific User object by ID
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a user object by ID"""

    # Attempt to retrieve the User object by its ID from storage
    user = storage.get("User", user_id)

    # If the User object does not exist, return a 404 Not Found error
    if user is None:
        abort(404)

    # Return a JSON response containing the User object's data
    return


# Define a route to delete a specific User object by ID
@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user object by ID"""

    # Attempt to retrieve the User object by its ID from storage
    user = storage.get("User", user_id)

    # If the User object does not exist, return a 404 Not Found error
    if user is None:
        abort(404)
    # Delete the User object, save changes, and return an empty JSON response
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Define a route to create a new User object
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User object"""

    # Get JSON data from the request
    data = request.get_json()

    # Check if the request contains valid JSON data
    if not data:
        abort(400, 'Not a JSON')

    # Check if 'email' and 'password' keys are present in the JSON data
    if 'email' not in data or 'password' not in data:
        abort(400, 'Missing email or password')

    # Create a new User object based on the JSON data
    user = User(**data)

    # Add the new User object to storage, save changes, and return its data
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object by ID"""

    # Attempt to retrieve the User object by its ID from storage
    user = storage.get("User", user_id)

    # If the User object does not exist, return a 404 Not Found error
    if user is None:
        abort(404)

    # Get JSON data from the request
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    # Update the User object's attributes based on the JSON data
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    # Save changes to the User object and return its updated data
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)

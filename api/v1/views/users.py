#!/usr/bin/python3
"""Creates a new view for User objects that
handles all default RESTFul API actions"""
from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views
from models import storage


# route to get all user objects
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """returns all state objects"""
    users = storage.all(User).values()
    user_l = [user.to_dict() for user in users]
    return jsonify(user_l)


# route for getting a user obj based on its id
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """returns user obj for the id input"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


# route for deleting a user obj
@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """deletes a user obj"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


# route for creating a user obj
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates a user obj"""
    if not request.get_json():
        abort(400, 'Not a JSON')

    """ transform the HTTP body request to a dictionary"""
    kwargs = request.get_json()
    if 'email' not in kwargs:
        abort(400, 'Missing email')
    if 'password' not in kwargs:
        abort(400, 'Missing password')

    user = User(**kwargs)
    user.save()

    return jsonify(user.to_dict()), 201


# route for updating a user obj
@app_views.route('users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """updates a user obj"""
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            abort(400, 'Not a JSON')

        """get JSON data from request"""
        new = request.get_json()
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        """update state obj with json data"""
        for key, value in new.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)

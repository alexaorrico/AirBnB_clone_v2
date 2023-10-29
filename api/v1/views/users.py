#!/usr/bin/python3
""" Module containing User View """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieves the list of all User objects.

        Returns:
            List of dictionaries representing User objects in JSON format.
    """
    users = [user.to_dict() for user in storage.all("User").values()]
    return jsonify(users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object based on `user_id`.

    Args:
        user_id (str): The UUID4 string representing a User object.

    Returns:
        Dictionary represention of a User object in JSON format.
        404 error if `user_id` is not linked to any User object.
    """
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object based on `user_id`.

    Args:
        user_id (str): The UUID4 string representing a User object.

    Returns:
        Returns an empty dictionary with the status code 200.
        404 error if `user_id` is not linked to any User object.
    """
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    user_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """ Creates a User object using HTTP body request fields.

    Returns:
        Returns the new User object as a  dictionary in JSON format
        with the status code 201.
        400 error if HTTP body request is not a valid JSON or if the dictionary
        passed does not contain the key `email` and/or `password`.
    """
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    if fields.get('email') is None:
        return "Missing email", 400
    if fields.get('password') is None:
        return "Missing password", 400
    new_user = User(**fields)
    new_user.save()
    """ May need to call `get` on new_user for all attributes to show """
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def edit_user(user_id):
    """ Edit a User object using `user_id` and HTTP body request fields.

    Args:
        user_id (str): The UUID4 string representing a User object.

    Returns:
        Returns the User object as a dictionary in JSON format with the
        status code 200.
        400 error if the HTTP body request is not a valid JSON.
        404 error if `user_id` is not linked to any User object.
    """
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    for key in fields:
        if key in ['id', 'email', 'created_at', 'update_at']:
            continue
        if hasattr(user_obj, key):
            setattr(user_obj, key, fields[key])
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200

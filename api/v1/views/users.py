#!/usr/bin/python3
"""
flask application module for retrieval of
User Objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    return (jsonify(
            [obj.to_dict() for obj in storage.all("User").values()]))

@app_views.route('/users/<string:<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieves a User object: <user_id>"""
    userToReturn = storage.get("User", user_id)
    if userToReturn is None:
        abort(404)
    return (jsonify(userToReturn.to_dict()))

@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """Deletes a User object: user_id"""
    userToDelete = storage.get("User", user_id)
    if userToDelete is None:
        abort(404)
    userToDelete.delete()
    storage.save()
    return (jsonify({}))

@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def post_user():
    """create a new User object in DB"""
    newUserData = request.get_json()
    if newUserData is None or type(newUserData) != dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    newEmail = newUserData.get('email')
    if newEmail is None:
        return (jsonify({'error': 'Missing email'}), 400)
    newPassword = newUserData.get('password')
    if newPassword is None:
        return (jsonify({'error': 'Missing password'}), 400)
    newUser = User(**newUserData)
    newUser.save()
    return (jsonify(newUser.to_dict()), 201)

@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user_by_id(user_id):
    """Updatea a User object: user_id"""
    putUserData = request.get_json()
    if putUserData is None or type(putUserData) != dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    UserToUpdate = storage.get("User", user_id)
    if UserToUpdate is None:
        abort(404)
    keysToIgnore = ['id', 'email', 'created_at', 'updated_at']
    for key, value in putUserData.items():
            if key in keysToIgnore:
                continue
            setattr(UserToUpdate, key, value)
    UserToUpdate.save()
    return (jsonify(UserToUpdate.to_dict()), 200)

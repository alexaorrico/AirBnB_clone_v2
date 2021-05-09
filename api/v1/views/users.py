#!/usr/bin/python3
""" new view for User """

from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def allusers():
    """ GET all users """
    users = []
    for user in storage.all('User').values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def getusers(user_id):
    """ GET user """
    user = storage.get('User', user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def deleteuser(user_id):
    """ DELETE user """
    user = storage.get('User', user_id)
    if user:
        user.delete()
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def createuser():
    """ POST to create user """
    user_dict = request.get_json()
    if not user_dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'email' not in user_dict:
        return (jsonify

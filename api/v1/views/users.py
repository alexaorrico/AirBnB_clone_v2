#!/usr/bin/python3
"""
flask application module for retrieval of
User Objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User

@app_views.route('/users',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    print("in correct route")
    if request.method == 'GET':
        returnedValue, code = User.api_get_all(
                    storage.all("User").values()
        )
    if request.method == 'POST':
        returnedValue, code = User.api_post(
                    ["email", "password"],
                    request.get_json(silent=True))
    return (jsonify(returnedValue), code)


@app_views.route('/users/<string:User_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def User_by_id(User_id):
    """handles User object: User_id"""
    if request.method == 'GET':
        returnedValue, code = User.api_get_single(
                        storage.get("User", User_id))
    if request.method == 'DELETE':
        returnedValue, code = User.api_delete(
                    storage.get("User", User_id))
    if request.method == 'PUT':
        returnedValue, code = User.api_put(
                    ['id', 'email', 'created_at', 'updated_at'],
                    request.get_json(silent=True),
                    storage.get("User", User_id))
    if code == 404:
        abort(404)
    storage.save()
    return (jsonify(returnedValue), code)

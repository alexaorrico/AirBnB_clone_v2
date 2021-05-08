#!/usr/bin/python3
"""
Create a new view for User objects that handles
all default RestFul API actions.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user():
    """Retrieve all objects"""
    l = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(l)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieve an object by id"""
    obj = storage.get(User, user_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete an object by id"""
    obj = storage.get(User, user_id)
    if obj:
        obj.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create an object"""
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if not body.get("email"):
        abort(400, "Missing email")
    if not body.get("password"):
        abort(400, "Missing password")
    obj = User(**body)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """ Update an object """
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    for k, v in body.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200

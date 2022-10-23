#!/usr/bin/python3
"""cities route"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/users/', strict_slashes=False, methods=['GET'])
def get_users():
    """Endpoint to retreive all users"""
    all_users = []
    users = storage.all(User)
    for v in users.values():
        all_users.append(v.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<string:user_id>', strict_slashes=False,)
def get_user(user_id):
    """Endpoint to retreive a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """Endpoint to delete a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def post_user():
    """Endpoint to create a user"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description='Missing email')
    if 'password' not in request.get_json():
        abort(400, description='Missing password')
    data = request.get_json()
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<string:user_id>',
                 strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """Endpoint to update a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore = ['id', 'email', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignore:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200

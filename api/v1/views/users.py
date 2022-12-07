#!/usr/bin/python3
"""
users
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users',
                 strict_slashes=False,
                 methods=['GET'])
def get_users():
    """ Get All users"""
    users = storage.all(User).values()

    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['GET'])
def get_user(user_id):
    """ Get user with Id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """ DELETE user With id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users',
                 strict_slashes=False,
                 methods=['POST'])
def post_user():
    """ Crate users"""
    try:
        body = request.get_json()

        if body is None:
            abort(400, description="Not a JSON")
        elif body.get('name') is None:
            abort(400, description='Missing name')
        else:
            obj = User(**body)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    except ValueError:
        abort(400, desciption="Not a JSON")


@app_views.route('/users/<user_id>', methods=["PUT"])
def update_user(user_id):
    """UPDATE a single users"""
    found = storage.get(User, user_id)
    if not found:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        else:
            invalid = ['id', 'created_at', 'updated_at','email']
            for key, value in req.items():
                if key not in invalid:
                    setattr(found, key, value)
            storage.save()
            return jsonify(found.to_dict()), 200
    except ValueError:
        abort(400, description="Not a JSON")




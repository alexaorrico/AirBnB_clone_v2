#!/usr/bin/python3
"""
    This is the users page handler for Flask.
"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request

from models.user import User


@app_views.route('/users', methods=['GET', 'POST'])
def users():
    """
        Flask route at /users.
    """
    if request.method == 'POST':
        kwargs = request.get_json()
        if not kwargs:
            return {"error": "Not a JSON"}, 400
        if "email" not in kwargs:
            return {"error": "Missing email"}, 400
        if "password" not in kwargs:
            return {"error": "Missing password"}, 400
        new_user = User(**kwargs)
        new_user.save()
        return new_user.to_dict(), 201

    elif request.method == 'GET':
        return jsonify([u.to_dict() for u in storage.all("User").values()])


@app_views.route('/users/<id>', methods=['GET', 'DELETE', 'PUT'])
def users_id(id):
    """
        Flask route at /users/<id>.
    """
    user = storage.get(User, id)
    if (user):
        if request.method == 'DELETE':
            user.delete()
            storage.save()
            return {}, 200

        elif request.method == 'PUT':
            kwargs = request.get_json()
            if not kwargs:
                return {"error": "Not a JSON"}, 400
            for k, v in kwargs.items():
                if k not in ["id", "email", "created_at", "updated_at"]:
                    setattr(user, k, v)
            user.save()
        return user.to_dict()
    abort(404)

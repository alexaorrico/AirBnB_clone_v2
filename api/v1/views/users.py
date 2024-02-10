#!/usr/bin/python3
"""
view for User objects that handles all default RestFul API actions
"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def handle_users():
    """Retrieves the list of all User objects or create a new User object"""
    if request.method == 'GET':
        return jsonify([obj.to_dict() for obj in storage.all("User").
                        values()]), 200
    if request.method == 'POST':
            if not request.get_json(silent=True):
                abort(400, "Not a JSON")
            if not request.get_json(silent=True).get('email'):
                abort(400, "Missing email")
            if not request.get_json(silent=True).get('password'):
                abort(400, "Missing password")
            kwargs = request.get_json(silent=True)
            new_user = User(**kwargs)
            new_user.save()
            return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_byid(user_id):
    """Retrieves a User object by id, delete or update a User object"""
    user_obj = storage.get("User", user_id)
    if user_obj:
        if request.method == 'GET':
            return jsonify(user_obj.to_dict()), 200
        elif request.method == 'DELETE':
            storage.delete(user_obj)
            storage.save()
            return {}, 200
        elif request.method == 'PUT':
            if not request.get_json(silent=True):
                abort(400, "Not a JSON")
            kwargs = request.get_json(silent=True)
            if kwargs:
                for key, value in kwargs.items():
                    if key not in ["id", "created_at", "updated_at"]:
                        setattr(user_obj, key, value)
                user_obj.save()
            return jsonify(user_obj.to_dict()), 200
    else:
        abort(404)

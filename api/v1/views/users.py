#!/usr/bin/python3
""" states view class """
from models import storage
from api.v1.views import app_views
from models.user import User
from flask import jsonify, request, abort, make_response


@app_views.route('/users', strict_slashes=False, methods=["GET", "POST"])
def get_users():
    """get all users or create a new user object"""
    users = storage.all("User")

    if request.method == "GET":
        return jsonify([obj.to_dict() for obj in users.values()])

    if request.method == "POST":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if request.get_json().get("email") is None:
            return make_response(jsonify({'error': 'Missing email'}), 400)
        if request.get_json().get("password") is None:
            return make_response(jsonify({'error': 'Missing password'}), 400)
        user = User(**request.get_json())
        user.save()
        return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def get_user_id(user_id=None):
    """ get certain city"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == "GET":
        return jsonify(user.to_dict())
    elif request.method == "DELETE":
        user.delete()
        storage.save()
        return jsonify({})
    elif request.method == "PUT":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, val in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, val)
        user.save()
        return jsonify(user.to_dict())

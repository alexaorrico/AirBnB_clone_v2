#!/usr/bin/python3
"""Handles RESTful API actions for User objects."""
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieve list of all User objects."""
    users = []
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieve a specific User object by ID."""
    user = None
    if user is None:
        abort(404)
    return jsonify(user)

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

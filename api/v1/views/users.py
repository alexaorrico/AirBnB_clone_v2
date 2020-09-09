#!/usr/bin/python3
"""dont trust the user"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.user import User


@app_views.route('/api/v1/users')
def get_users():
    """get em"""
    lizt = []
    users = storage.all(User).values()
    for user in users:
        lizt.append(user.to_dict())
    return jsonify(lizt)

@app_views.route('/api/v1/users/<user_id>')
def get_a_user():
    """get one"""
    lizt = []
    users = storage.all(User).values()
    for user in users:
        if user.id == user_id:
            lizt = user.to_dict()
            return jsonify(lizt)
    return jsonify({"error": "Not found"}), 404

@app_views.route('/api/v1/users/<user_id>', methods=['DELETE'])
def del_a_user():
    """remove one"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

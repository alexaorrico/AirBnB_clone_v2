#!/usr/bin/python3
"""dont trust the user"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, Blueprint
from models.user import User


@app_views.route('/users')
def get_users():
    """get em"""
    lizt = []
    users = storage.all(User).values()
    for user in users:
        lizt.append(user.to_dict())
    return jsonify(lizt)


@app_views.route('/users/<user_id>')
def get_a_user(user_id):
    """get one"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    ret = users.to_dict()
    return jsonify(ret)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def del_a_user(user_id):
    """remove one"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    storage.delete(users)
    storage.save()
    return jsonify({}), 200

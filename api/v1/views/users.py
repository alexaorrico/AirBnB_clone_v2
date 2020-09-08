#!/bin/bash python3
""" user view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, render_template, abort
from models import storage
from models.user import User
from models.base_model import BaseModel


@app_views.route('/users', methods=["GET"], strict_slashes=False)
def get_all_users():
    """ retrieves all user objects """
    output = []
    users = storage.all(User).values()
    for user in users:
        output.append(user.to_dict())
    return (jsonify(output))


@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def get_a_user(user_id):
    """ retrieves one unique user object """
    users = storage.all(User).values()
    for user in users:
        if user.id == user_id:
            output = user.to_dict()
            return (jsonify(output))
    abort(404)


@app_views.route('/users/<user_id>', methods=["GET", "DELETE"],
                 strict_slashes=False)
def del_a_user(user_id):
    """ delete one unique user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    result = make_response(jsonify({}), 200)
    return result

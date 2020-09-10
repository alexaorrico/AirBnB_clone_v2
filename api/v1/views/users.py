#!/usr/bin/python3
"""Users """

from flask import jsonify, request, abort, make_response
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """get users"""
    users = []
    for user in storage.all('User').values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """get specified user"""
    users = storage.all("User").values()
    for user in users:
        if user.id == user_id:
            return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """delete user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    response = make_response(jsonify({}), 200)
    return response


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def post_user():
    """create a user"""
    djson = request.get_json()
    if not djson:
        return make_response("Not a JSON", 400)
    if "email" not in djson:
        return make_response("Missing email", 400)
    if "password" not in djson:
        return make_response("Missing password", 400)
    new_user = User(**djson)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """update user based on ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    json = request.get_json()
    if not djson:
        return make_response("Not a JSON", 400)
    for key, value in djson.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)


if __name__ == "__main__":
    pass

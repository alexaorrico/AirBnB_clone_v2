#!/usr/bin/python3
""" All Users """
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def all_users():
    """ return all Users of the base """
    dic = []
    users = storage.all(User).items()
    for key, value in users:
        dic.append(value.to_dict())
    return jsonify(dic)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_id(user_id):
    """return the user id """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Delete method """
    state = storage.get(User, user_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Create a User with Post method """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    kwargs = request.get_json()
    user = User(**kwargs)
    storage.new(user)
    storage.save()
    return (jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def upd_user(user_id):
    """ Update an User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    json_content = request.get_json()
    if json_content is None:
        abort(400, description='Not a JSON')
    for key, value in json_content.items():
        if key != 'id' and key != 'created_ad' and key != 'updated_at':
            setattr(user, key, value)
    storage.save()
    return (jsonify(user.to_dict()), 200)

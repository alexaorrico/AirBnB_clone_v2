#!/usr/bin/python3
"""view for users"""


from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


@app_views.route('/users', strict_slashes=False)
def users():
    """return list of all objects User"""
    new_list = list()
    lst_states = storage.all('User')
    for value in lst_states.values():
        new_list.append(value.to_dict())
    return jsonify(new_list)


@app_views.route('/users/<user_id>', strict_slashes=False)
def users_id(user_id):
    """Return dictionary of specific user"""
    ret = storage.get("User", user_id)
    if ret:
        return ret.to_dict()
    abort(404)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """Deletes an specific user"""
    ret = storage.get('User', user_id)
    if ret:
        storage.delete(ret)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_User():
    """Create a new user"""
    from models.user import User
    content = request.get_json(force=True, silent=True)
    if not content:
        abort(400, "Not a JSON")
    name_user = content.get('name')
    if "email" not in content.keys():
        abort(400, "Missing email")
    if "password" not in content.keys():
        abort(400, "Missing password")

    new_instance = User(name=name_user)
    return jsonify(new_instance.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """Update a user by a given ID"""
    new_user = storage.get('User', user_id)
    if not new_user:
        abort(404)

    content = request.get_json(force=True, silent=True)
    if not content:
        abort(400, "Not a JSON")

    to_ignore = ['id', 'email', 'created_at', 'update_at']
    for key, value in content.items():
        if key in to_ignore:
            continue
        else:
            setattr(new_user, key, value)
    storage.save()
    return jsonify(new_user.to_dict()), 200

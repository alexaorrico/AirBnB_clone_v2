#!/usr/bin/python3
"""

Flask web server creation to handle api petition-requests

"""
from flask import jsonify, abort
from flask import request
from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def all_users():
    """
    Retrieves the list of all User objects
    """
    objects = storage.all("User")
    list_obj = []
    for obj in objects.values():
        list_obj.append(obj.to_dict())
    return jsonify(list_obj)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def some_user(user_id):
    """
    Retrieves a User object if id is linked to some User object
    """
    some_objs = storage.get(classes["User"], user_id)
    if some_objs is None:
        abort(404)
    some_objs = some_objs.to_dict()
    return jsonify(some_objs)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_user(user_id):
    """
    Deletes a User object if id is linked to some User object
    """
    some_objs = storage.get(classes["User"], user_id)
    if some_objs is None:
        abort(404)
    storage.delete(some_objs)
    storage.save()
    return jsonify({})


@app_views.route('/users/', strict_slashes=False, methods=['POST'])
def post_user():
    """
    Create a new User object
    """
    data_json = request.get_json(force=True, silent=True)
    if (type(data_json) is not dict):
        abort(400, "Not a JSON")
    if "email" not in data_json:
        abort(400, "Missing email")
    if "password" not in data_json:
        abort(400, "Missing password")
    else:
        new_user = classes["User"](**data_json)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def put_user(user_id):
    """
    Update a User object
    """
    obj = storage.get(classes["User"], user_id)
    if obj is None:
        abort(404)
    data_json = request.get_json(force=True, silent=True)
    if (type(data_json) is not dict):
        abort(400, "Not a JSON")
    for key, value in data_json.items():
        if key in ["id", "email", "created_at", "updated_at"]:
            continue
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())

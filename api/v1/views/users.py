#!/usr/bin/python3
"""view of State object"""
from api.v1.views import app_views
from models import storage, user
from flask import jsonify, abort, request


@app_views.route('/users', methods=["GET"])
def user_ret():
    """return json User objects"""
    user_list = []
    all_objs = storage.all("User")
    for obj in all_objs.values():
        user_list.append(obj.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=["GET"])
def user_get_by_id(user_id):
    """return json State objects by id"""
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=["DELETE"])
def user_delete(user_id=None):
    """delete an object by id"""
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=["POST"])
def post_user_obj():
    """add new state object"""
    dic = {}
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, "Not a JSON")
    if "password" not in dic.keys():
        abort(400, "Missing password")
    if "email" not in dic.keys():
        abort(400, "Missing email")
    new_user = user.User()
    for k, v in dic.items():
        setattr(new_user, k, v)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=["PUT"])
def update_user_obj(user_id=None):
    """update new state object"""
    dic = {}
    list_key = ['id', 'email', 'created_at', 'updated_at']
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, "Not a JSON")
    for key, value in dic.items():
        if key not in list_key:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200

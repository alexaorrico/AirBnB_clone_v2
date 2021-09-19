#!/usr/bin/python3
""" View User """

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User


@app_views.route("/users", methods=["GET"])
def userAll():
    """Retrieves all users with a list of objects"""
    ll = []
    s = storage.all('User').values()
    for v in s:
        ll.append(v.to_dict())
    return jsonify(ll)


@app_views.route("/users/<id>", methods=["GET"])
def userId(id):
    """id users retrieve json object"""
    ll = []
    s = storage.all('User').values()
    for v in s:
        if v.id == id:
            ll.append(v.to_dict())
    if not ll:
        return abort(404)
    return jsonify(ll)


@app_views.route("/users/<id>", methods=["DELETE"])
def userDel(id):
    """delete users with id"""
    user = storage.get("User", id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def userPost():
    """ POST a new users"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.json:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.json:
        return jsonify({"error": "Missing password"}), 400
    x = request.get_json()
    s = User(**x)
    s.save()
    return jsonify(s.to_dict()), 201


@app_views.route('/users/<id>', methods=['PUT'])
def userPut(id):
    """ Update a user object """
    ignore = {"id", "email", "created_at", "updated_at"}
    user = storage.get("User", id)
    if user is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    x = request.get_json()
    for k, v in x.items():
        if k not in ignore:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200

#!/usr/bin/python3
""" functions GET, PUT, POST & DELETE """

from flask import jsonify, request, abort
from api.v1.views import app_views
from models.users import User
from models import storage


@app_views.route('/api/v1/users', methods=['GET'])
def get_all():
    """ get all the states """
    user = []
    all_users = storage.all(User)
    for i in all_users:
        user.append(all_users[i].to_dict())
    return jsonify(user)


@app_views.route('/api/v1/users/<user_id>', methods=['GET'])
def get_id(user_id):
    """ get status by id """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict()), 200
    abort(404)


@app_views.route("/api/v1/users/<user_id>", methods=['DELETE'])
def del_id(user_id):
    """ delete user by id """
    user = storage.get(User, user_id)
    storage.delete(user)
    storage.save()
    if not user:
        abort(404)
    return ({}), 200


@app_views.route('/api/v1/users', methods=['POST'])
def add():
    """ add statte to storage """
    if request.json:
        content = request.get_json()
        if "email" not in content.keys():
            return jsonify("Missing email"), 400
        if "password" not in content.keys():
            return jsonify("Missing password"), 400
        else:
            add_user = User(**content)
            add_user.save()
            return jsonify(add_user.to_dict()), 201
    return jsonify("Not a JSON"), 400


@app_views.route('/api/v1/users/<user_id>', methods=['PUT'])
def update(user_id):
    """ update states with id """
    dic = storage.all(User)
    for i in dic:
        if dic[i].id == user_id:
            if request.json:
                ignore = ["id", "email", "created_at", "updated_at"]
                content = request.get_json()
                for items in content:
                    if items not in ignore:
                        setattr(dic[i], items, content[items])
                dic[i].save()
                return jsonify(dic[i].to_dict())
            else:
                return jsonify("Not a JSON"), 400
    abort(404)

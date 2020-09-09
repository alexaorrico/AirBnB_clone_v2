#!/usr/bin/python3
""" api for user """
from models.base_model import BaseModel, Base
from flask import jsonify, abort, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def allusers(user_id=None):
    """ show all users and one user object"""
    if user_id is None:
        lista = []
        for v in storage.all(User).values():
            lista.append(v.to_dict())
        return (jsonify(lista))
    else:
        flag = 0
        for v in storage.all(User).values():
            if v.id == user_id:
                attr = (v.to_dict())
                flag = 1
        if flag == 0:
            abort(404)
        else:
            return (jsonify(attr))


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_users(user_id=None):
    """ delete a user object """
    dicti = {}
    flag = 0
    for v in storage.all(User).values():
        if v.id == user_id:
            storage.delete(v)
            storage.save()
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(dicti), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_task_users():
    """ create a user object """
    if not request.json:
        abort(400, "Not a JSON")
    if not 'email' in request.json:
        abort(400, "Missing email")
    if not 'password' in request.json:
        abort(400, "Missing password")
    result = request.get_json()
    obj = User()
    for k, v in result.items():
        setattr(obj, k, v)
    storage.new(obj)
    storage.save()
    var = obj.to_dict()
    return (jsonify(var), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_task_users(user_id=None):
    """ change atributes of user object """
    lista = ["first_name", "last_name", "password"]
    if not request.json:
        abort(400, "Not a JSON")
    result = request.get_json()
    flag = 0
    for values in storage.all(User).values():
        if values.id == user_id:
            for scurity in lista:
                if scurity in request.json:
                    for k, v in result.items():
                        setattr(values, k, v)
                        storage.save()
                        attr = (values.to_dict())
                        flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(attr), 200)

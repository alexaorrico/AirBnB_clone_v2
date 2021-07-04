#!/usr/bin/python3
""" State restful api """
from models.base_model import BaseModel, Base
from flask import jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def allstates(state_id=None):
    """ Retrieve one object or all objects of State """
    if state_id is None:
        lista = []
        for v in storage.all(State).values():
            lista.append(v.to_dict())
        return (jsonify(lista))
    else:
        flag = 0
        for v in storage.all(State).values():
            if v.id == state_id:
                attr = (v.to_dict())
                flag = 1
        if flag == 0:
            abort(404)
        else:
            return (jsonify(attr))


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete(state_id=None):
    """ Delete a state object """
    if state_id is None:
        abort(404)
    dicti = {}
    flag = 0
    for v in storage.all(State).values():
        if v.id == state_id:
            storage.delete(v)
            storage.save()
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(dicti), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_task():
    """ create a state object """
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    result = request.get_json()
    obj = State()
    for k, v in result.items():
        setattr(obj, k, v)
    storage.new(obj)
    storage.save()
    var = obj.to_dict()
    return (jsonify(var), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_task(state_id=None):
    """ Change atributes of state object """
    if not request.json or 'name' not in request.json:
        abort(400, "Not a JSON")
    if state_id is None:
        abort(404)

    result = request.get_json()
    flag = 0
    for values in storage.all(State).values():
        if values.id == state_id:
            for k, v in result.items():
                setattr(values, k, v)
                storage.save()
                attr = (values.to_dict())
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(attr), 200)

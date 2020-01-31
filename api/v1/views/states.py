#!/usr/bin/python3
""" Create a new view for State that handles all default RestFul API """

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import Flask, jsonify, abort, request


@app_views.route('/states/',  methods=['GET'], strict_slashes=False)
def States_Get():
    """ Retrieve all the states"""

    data = storage.all('State')
    var = []

    for value in data.values():
        var.append(value.to_dict())

    return jsonify(var)


@app_views.route('/states/<state_id>',  methods=['GET'], strict_slashes=False)
def States_Id(state_id):
    """ Retrieve an state by id """
    data = storage.all('State')
    for key, value in data.items():
        key = key.split(".")
        if key[-1] == state_id:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def State_Delete(state_id):
    """ Retrieve an state by id """
    data = storage.all('State')
    del_state = storage.get('State', state_id)
    if del_state is None:
        abort(404)
    storage.delete(del_state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/',  methods=['POST'], strict_slashes=False)
def States_Post():
    """ Post """

    data = request.get_json()

    if not data:
        return jsonify({"message": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"message": "Missing name"}), 400

    name_state = {"name": data["name"]}
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>',  methods=['PUT'], strict_slashes=False)
def State_Put(state_id):
    """ Put """
    data = storage.get('State', state_id)
    data_req = request.get_json()

    if data is None:
        abort(404)
    if not data_req:
        return jsonify({"message": "Not a JSON"}), 400

    for key, value in data_req.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        setattr(data, key, value)
    data.save()
    return jsonify(data.to_dict()), 200

#!/usr/bin/python3
""" View State """
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request


@app_views.route("/states", methods=["GET"])
def statesAll():
    """Retrieves the list of all State objects"""
    all_states = []
    sto = storage.all('State').values()
    for val in sto:
        all_states.append(val.to_dict())
    return jsonify(all_states)


@app_views.route("/states/<id>", methods=["GET"])
def stateId(id):
    """id state retrieve json object"""
    sto = storage.all('State').values()
    for val in sto:
        if val.id == id:
            return jsonify(val.to_dict())
    abort(404)


@app_views.route("/states/<id>", methods=["DELETE"])
def stateDel(id):
    """delete state with id"""
    state = storage.get('State', id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def statePost():
    """Creates a new state"""
    state_data = request.get_json()
    if state_data is None:
        abort(400, "Not a JSON")
    if not state_data.get('name'):
        abort(400, "Missing name")
    new_state = State(**state_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<id>', methods=['PUT'])
def statePut(id):
    """Update a State object"""
    x = request.get_json()
    if x is None:
        abort(400, "Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    state = storage.get("State", id)
    if state is None:
        abort(404)
    for k, v in x.items():
        if k not in ignore:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200

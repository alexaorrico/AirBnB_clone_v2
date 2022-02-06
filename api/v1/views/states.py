#!/usr/bin/python3
"""State"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request


@app_views.route("/states", methods=["GET"])
def states_all():
    """Retrieves all states with a list of objects"""
    lists = []
    s = storage.all('State').values()
    for v in s:
        lists.append(v.to_dict())
    return jsonify(lists)


@app_views.route("/states/<id>", methods=["GET"])
def state_id(id):
    """id state retrieve json object"""
    date = storage.all('State').values()
    for x in date:
        if x.id == id:
            return jsonify(x.to_dict())
    abort(404)


@app_views.route("/states/<id>", methods=["DELETE"])
def state_delete(id):
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
    date = request.get_json()
    if date is None:
        abort(400, "Not a JSON")
    if not date.get('name'):
        abort(400, "Missing name")
    nwe_date = State(**date)
    storage.new(nwe_date)
    storage.save()
    return jsonify(storage.get(State, nwe_date.id).to_dict()), 201


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
    for x, y in x.items():
        if x not in ignore:
            setattr(state, x, y)
    state.save()
    return jsonify(storage.get(State, state.id).to_dict()), 200

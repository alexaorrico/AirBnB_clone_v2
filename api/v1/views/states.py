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


@app_views.route("/states/<state_id>", methods=["GET"])
def state_id0(state_id):
    """id state retrieve json object"""
    state_obj = storage.get(State, state_id)
    if state_obj:
        return jsonify(state_obj.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def state_delete(state_id):
    """delete state with id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'])
def statePost():
    """Creates a new state"""
    date = request.get_json()
    if date is None:
        abort(400, "Not a JSON")
    elif "name" not in date.keys():
        abort(400, "Missing name")
    else:
        nwe_date = State(**date)
        storage.new(nwe_date)
        nwe_date.save()
        return jsonify(nwe_date.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def statePut(state_id):
    """Update a State object"""
    state = storage.get("State", state_id)
    x = request.get_json()
    if state:
        if x:
            ignore = ['id', 'created_at', 'updated_at']
            for x, y in x.items():
                if x != ignore:
                    setattr(state, x, y)
            state.save()
            return jsonify(state.to_dict()), 200
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)

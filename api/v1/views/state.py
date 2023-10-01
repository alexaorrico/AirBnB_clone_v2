#!/usr/bin/python3
"""Defines views for the state route"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models import State


@app_views.route('/states', methods=['GET', 'POST'])
def states():
    """Returns a json of all states in the database"""
    if request.method == 'GET':
        allstates = storage.all("State").values()
        print("in")
        return jsonify([state.to_dict() for state in allstates])
    
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return 'Not a JSON', 400
        if 'name' not in data:
            return 'Missing name', 400
        state = State(**data)
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def states_id(state_id):
    """Returns a json of specific states
       GET::
            Return the state with the id provided.
       DELETE::
            Deletes a state by its state id.
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 201
    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return 'Not a JSON', 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save
        return jsonify(state.to_dict(), 200)

#!/usr/bin/python3
"""Defines views for the state route"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models import state


@app_views.route('/states', method=['GET','POST'])
def states():
    """Returns a json of all states in the database"""
    if request.method == 'GET':
        allstates = storage.all("States").values()
        return jsonify([state.to_dict() for state in allstates])
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
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
        return jsonify({}), 200

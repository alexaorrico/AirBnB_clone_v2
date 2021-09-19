#!/usr/bin/python3
""" Handles all state objects for the api """
import re
from flask import jsonify, abort, request, Response
from sqlalchemy.sql.expression import insert
from models.state import State
from models import storage
from api.v1.views import app_views

@app_views.route('/states/', strict_slashes=False)
def states():
    """display the states and cities listed in alphabetical order"""
    states = storage.all(State)
    new_dict = []
    for state in states:
        new_dict.append(states[state].to_dict())
    return jsonify(new_dict) 

@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def state_by_id(state_id=None):
    """ gets a state by the given state_id """
    state = storage.get(State, state_id)
    if state is not None:
        state = state.to_dict()
        return jsonify(state)
    else:
        abort(404)

@app_views.route('/states/<state_id>', methods=["DELETE"], strict_slashes=False)
def delete_state(state_id=None):
    """ Deletes state by given id """
    state =  storage.get(State, state_id)
    if state is not None:
        storage.delete(state)
    else:
        abort(404)

@app_views.route('/states/', methods=["POST"], strict_slashes=False)
def post_state():
    """ Creates given json obj in db with given id """
    if request.is_json is False:
        return Response("Not a JSON", status=400)
    new_state_dict = request.get_json()
    if "name" not in new_state_dict.keys():
        return Response("Missing name", status=400)
    instance = State(**new_state_dict)
    instance.save()
    return jsonify(instance.to_dict()), 201




@app_views.route('/states/<state_id>', methods=["PUT"], strict_slashes=False)
def put_state(state_id=None):
    """ Updates a state object with the given id and json """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.is_json is False:
        return Response("Not a JSON", status=400)
    new_state_dict = request.get_json()
    for key, value in new_state_dict.items():
        setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
    # TODO: setatr for the update

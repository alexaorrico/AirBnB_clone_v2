#!/usr/bin/python3
"""new view for State objects that handles all """

from flask import Flask, abort, jsonify, make_response
from flask import request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def all_state():
    """Return all states"""
    states = storage.all(State).values()
    list_state = []
    for state_ in states:
        list_state.append(state_.to_dict())
    return jsonify(list_state)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_id(state_id=None):
    """return states"""
    if state_id is not None:
        my_state_obj = storage.get(State, state_id)
        if my_state_obj is None:
            abort(404)
        else:
            return jsonify(my_state_obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_delete(state_id=None):
    """delete state"""
    if state_id is not None:
        my_state_obj = storage.get(State, state_id)
        if my_state_obj is None:
            abort(404)
        else:
            storage.delete(my_state_obj)
            return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'])
def state_post():
    """POST state"""
    my_json = request.get_json(silent=True)
    if my_json is not None:
        if "name" in my_json:
            name = my_json["name"]
            new_state = State(name=name)
            new_state.save()
            return make_response(jsonify(new_state.to_dict()), 201)
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route('states/<state_id>', methods=['PUT'])
def update_state(state_id=None):
    """PUT state"""
    if state_id is not None:
        my_state_obj = storage.get(State, state_id)
        if my_state_obj is None:
            abort(404)
        else:
            update_ = request.get_json(silent=True)
            if update_ is not None:
                for key, value in update_.items():
                    setattr(my_state_obj, key, value)
                    my_state_obj.save()
                return make_response(jsonify(my_state_obj.to_dict()), 200)
            else:
                abort(400, "Not a JSON")

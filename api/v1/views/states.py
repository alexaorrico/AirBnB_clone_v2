#!/usr/bin/python3
""" STATE VIEW """
from api.v1.views import states_views
from flask import jsonify, abort, request
from models.state import State
from models import storage
import json
from datetime import datetime


@states_views.route(
        '/states', methods=["GET"], strict_slashes=False
        )
def all_states():
    """ Return all states objects in DB """
    all_states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(all_states)


@states_views.route(
        '/states/<state_id>', methods=["GET"], strict_slashes=False
        )
def single_state(state_id):
    """ Returns state that matches with provided ID """
    all_states = [state.to_dict() for state in storage.all(State).values()]
    state = [state for state in all_states if state.get("id") == state_id]
    if len(state) != 0:
        return jsonify(state[0])
    abort(404)


@states_views.route(
        '/states/<state_id>', methods=["DELETE"], strict_slashes=False
        )
def delete_state(state_id):
    """ Deletes state that matches with provided ID """
    sta = [st for st in storage.all(State).values() if str(st.id) == state_id]
    if len(sta) != 0:
        storage.delete(sta[0])
        storage.save()
        return jsonify({}), 200
    abort(404)


@states_views.route(
        '/states/', methods=["POST"], strict_slashes=False
        )
def add_state():
    """ Adds state object to DB """
    try:
        data = request.get_json()
    except json.JSONDecodeError:
        abort(400, description='Not a JSON')
    if "name" not in data:
        abort(400, description='Missing name')
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@states_views.route(
        '/states/<state_id>', methods=["PUT"], strict_slashes=False
        )
def update_state(state_id):
    """Updates state object"""
    sta = [st for st in storage.all(State).values() if str(st.id) == state_id]
    if len(sta) == 0:
        abort(404)
    try:
        data = request.get_json()
    except json.JSONDecodeError:
        abort(400, description='Not a JSON')
    sta[0].__dict__.update(data)
    sta[0].updated_at = datetime.utcnow()
    storage.save()
    return jsonify(sta[0].to_dict()), 200

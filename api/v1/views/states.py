#!/usr/bin/python3
"""this is the state view for the API"""
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.state import State

ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
"""HTTP methods allowed for states"""


@app_views.route('/states', methods=ALLOWED_METHODS)
@app_views.route('/states/<state_id>', methods=ALLOWED_METHODS)
def handle_states(state_id=None):
    """handles all allowed HTTP methods to state(id)."""
    handlers = {
        'GET': get_states,
        'DELETE': del_state,
        'POST': add_state,
        'PUT': update_state,
    }
    if request.method in handlers:
        return handlers[request.method](state_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_states(state_id=None):
    """uses the GET method to retrieve a state(id)."""
    all_states = storage.all(State).values()
    if state_id:
        unique_state = [state for state in all_states if state.id == state_id]
        if unique_state:
            return jsonify(unique_state[0].to_dict())
        else:
            raise NotFound()
    else:
        all_states_dicts = [state.to_dict() for state in all_states]
        return jsonify(all_states_dicts)


def del_state(state_id=None):
    """uses the DELETE method to delete a state(id)."""
    all_states = storage.all(State).values()
    unique_state = [state for state in all_states if state.id == state_id]
    if unique_state:
        state_to_delete = unique_state[0]
        storage.delete(state_to_delete)
        storage.save()

        return jsonify({}), 200
    raise NotFound()


def add_state(state_id=None):
    """uses the POST method to add a new state"""
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    A
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()),  201


def update_state(state_id=None):
    """uses the PUT method to update state."""
    keys_to_update = ('id', 'created_at', 'updated_at')
    all_states = storage.all(State).values()
    upd_state = [state for state in all_states if state.id == state_id]
    if unique_state:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        for key, value in data.items():
            if key not in keys_to_update:
                setattr(upd_state[0], key, value)

        upd_state[0].save()

        return jsonify(upd_state[0].to_dict()), 200

    raise NotFound()

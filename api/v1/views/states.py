#!/usr/bin/python3
""" Handle RESTful API actions for State objects """
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_objects():
    """ Retrieves the list of all State objects """
    state_objs = storage.all(State)
    state_json = []
    for obj in state_objs.values():
        state_json.append(obj.to_dict())
    return jsonify(state_json)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states_object(state_id):
    """ Return a State object matching the given state_id """
    try:
        state_obj = storage.get(State, state_id)
        return jsonify(state_obj.to_dict())
    except:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_object(state_id):
    """ Delete a State object """
    try:
        state_obj = storage.get(State, state_id)
        storage.delete(state_obj)
        storage.save()
        return make_response(jsonify({}), 200)
    except:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state_object():
    """ Create a new State object """
    if not request.get_json():
        abort(400, description='Not a JSON')
    elif 'name' not in request.get_json():
        abort(400, description='Missing name')
    else:
        content = request.get_json()
        state = State()
        state.name = content['name']
        state.save()
        return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_object(state_id):
    """ Update the attributes of a State object """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    content = request.get_json()
    nope = ['id', 'created_at', 'updated_at']
    for key, value in content.items():
        if key not in nope:
            setattr(state_obj, key, value)
    storage.save()
    return make_response(jsonify(state_obj.to_dict()), 200)

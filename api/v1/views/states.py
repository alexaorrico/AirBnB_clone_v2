#!/usr/bin/python3
""" State views """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ Return all states """
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())

    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
    """ Return a state from the id supplied """
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ Deletes a state by id """
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def new_state():
    """ Creates a new state """
    if not request.get_json():
        abort(400, descrption="Not a JSON")

    if not request.get_json().get('name'):
        abort(400, description="Missing name")

    state = State()
    state.name = request.get_json()['name']
    state.save()
    
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates the state specified by id """
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for key, value in request.get_json().items():
        if key == "id" or key == "created_at" or key == "updated_at":
            continue
        else:
            setattr(state, key, value)

    storage.save()

    return make_response(jsonify(state.to_dict()), 200)

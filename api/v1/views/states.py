#!/usr/bin/python3
"""
View for state
"""
from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'],
                 strict_slashes=False)
def get_states():
    """
    retrieve an object into a valid JSON
    """
    all_states = storage.all(State)
    my_list = []
    for obj in all_states:
        my_list.append(all_states[obj].to_dict())
    return jsonify(my_list)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    """
    Retrieves a State object: GET /api/v1/states/<state_id>
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """
    Deletes a State object
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """
    Creates a State: POST /api/v1/states
    """
    if not request.json:
        return jsonify('Not a JSON'), 400
    if 'name' not in request.json:
        return jsonify('Missing name'), 400
    state = State(**request.get_json())
    storage.new(state)
    storage.save()
#    return jsonify(state.to_dict()), 201
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_by_id(state_id):
    """
    Updates a State object
    """
    state = storage.get("State", state_id)
    print(state)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    for key, value in request.get_json().items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
#    return make_response(jsonify(state.to_dict()), 200)

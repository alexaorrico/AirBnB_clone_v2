from flask import Flask
from models import storage
from models.state import State
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/states", methods=["GET"])
def get_states():
    """get state information for all states"""
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_states_by_id(state_id):
    """get state information for specific states"""
    state = storage.get(State, state_id)
    if state != None:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """deletes a state based on its state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return {}


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """ create a state"""
    createJson = request.get_json()
    if createJson is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if not 'name' in createJson.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**createJson)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """update a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr is not 'id' or attr is not 'created_at' or attr is not 'updated_at':
            setattr(state, attr, val)
    storage.save()
    return jsonify(state.to_dict())

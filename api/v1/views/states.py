#!/usr/bin/python3
""" Objects that handle default RESTFUL API actions for states """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves the list of all State objects """
    all_states = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(all_states)

@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State object  """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """ Deletes a State object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})

@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """ Creates a State """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    js = request.get_json()
    obj = State(**js)
    obj.save()
    return jsonify(obj.to_dict()), 201

@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def post_state(state_id):
    """ Updates a State object """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())

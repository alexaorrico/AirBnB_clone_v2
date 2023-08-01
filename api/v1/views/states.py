#!/usr/bin/python3
""" new State object view. Handles default RESTful API actions"""
from flask import jsonify
from flask import abort
from api.v1.views import app_views
from models import storage
from flask import request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id=None):
    """Retrieves list of all State objects in storage. If id is given,
    retrieves State based on given id"""
    states = [state.to_dict() for state in storage.all("State").values()]
    if state_id is None:
        return jsonify(states)
    else:
        obj = storage.get("State", state_id)
        if obj is None:
            abort(404)
        return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """Deletes State objects based on given id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a State object based on get_json request"""
    state = State()
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data.keys():
            abort(400, 'Missing name')
    for key, value in data.items():
        setattr(state, key, value)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id=None):
    """Updates a State object based on id using response from get_json"""
    state = storage.get("State", state_id)
    data = request.get_json(silent=True)
    if state is None:
        abort(404)
    if data is None:
        abort(400, "Not a JSON")
    else:
        for key, value in data.items():
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200

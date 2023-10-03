#!/usr/bin/python3
"""script that starts a Flask web application"""


from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State

app = Flask(__name__)


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all('State')
    state_list = []
    for state in states.values():
        state_list.append(state.to_dict())
    return jsonify(state_list), 200


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """Retrieves a State object with the id linked to it"""
    state_dict = storage.all('State')
    state = state_dict.get('State' + "." + state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """Deletes a State object"""
    obj = storage.get('State', state_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a State"""
    result = request.get_json()
    if not result:
        abort(400, {"Not a JSON"})
    if 'name' not in result:
        abort(400, {"Missing name"})
    obj = State(name=result['name'])
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id=None):
    """Updates a State object"""
    result = request.get_json()
    if not result:
        abort(400, {"Not a JSON"})
    obj = storage.get('State', state_id)
    if obj is None:
        abort(404)
    invalid_keys = ["id", "created_at", "updated_at"]
    for key, value in result.items():
        if key not in invalid_keys:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200

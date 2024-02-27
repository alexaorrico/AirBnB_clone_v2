#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API"""

from models.base_model import BaseModel
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def states():
    """getting all members of state"""
    state_object = storage.all('State').values()
    state_list = []
    for item in state_object:
        state_list.append(item.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<string:state_id>",
                 methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """getting a particular state"""
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    return jsonify(state_object.to_dict()), '200'


@app_views.route("/states/<state_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """Deletes a State object:: DELETE"""
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    storage.delete(state_object)
    storage.save()
    return jsonify({}), '200'


@app_views.route("/states",
                 methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State: POST /api/v1/states"""
    if request.is_json:
        """do something"""
        json_data = request.get_json()
        if 'name' in json_data:
            """do create a new State"""
            new_state_name = json_data['name']
            new_state = State(name=new_state_name)
            new_state.save()
            return jsonify(new_state.to_dict()), 201
        else:
            return jsonify({'error': 'Missing name'}), 400
    else:
        return jsonify({'error': 'Not a JSON'}), 400


@app_views.route("/states/<string:state_id>",
                 methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """Updates a State object: PUT /api/v1/states/<state_id>"""
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    if request.is_json:
        json_data = request.get_json()
        for key, value in json_data.items():
            if key == 'id' or key == 'created_at' or key == 'updated_at':
                pass
            else:
                setattr(state_object, key, value)
            storage.save()
        return jsonify(state_object.to_dict()), 200
    else:
        return jsonify({'error': 'Not a JSON'}), 400

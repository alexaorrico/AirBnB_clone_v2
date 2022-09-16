#!/usr/bin/python3
"""view states object"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states', strict_slashes=False)
def states():
    """return list of all objects State"""
    new_list = list()
    lst_states = storage.all('State')
    for value in lst_states.values():
        new_list.append(value.to_dict())
    return jsonify(new_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def states_id(state_id):
    """Return dictionary of specific state"""
    ret = storage.get("State", state_id)
    if ret:
        return ret.to_dict()
    abort(404)


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """Deletes an specific state"""
    ret = storage.get('State', state_id)
    if ret:
        storage.delete(ret)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Create a new state"""
    from models.state import State
    content = request.get_json()
    if not content:
        abort(400, "Not a JSON")
    name_city = content.get('name')
    if "name" not in content.keys():
        abort(400, "Missing name")

    new_instance = State(name=name_city)
    return jsonify(new_instance.to_dict()), 200


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """Update a state by a given ID"""
    new_state = storage.get('State', state_id)
    if not new_state:
        abort(404)
    content = request.get_json()

    if not content:
        abort(400, "Not a JSON")
    to_ignore = ['id', 'created_at', 'update_at']
    for key, value in content.items():
        if key in to_ignore:
            continue
        else:
            setattr(new_state, key, value)
    storage.save()
    return jsonify(new_state.to_dict()), 200

#!/usr/bin/pyhton3
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects: GET /api/v1/states"""
    dict_state = storage.all("State")
    my_list = []
    for key, obj in dict_state.items():
        my_list.append(obj.to_dict())
    return jsonify(my_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def object_state(state_id, strict_slashes=False):
    """Retrieves a State object"""
    object_state = storage.get("State", state_id)
    if object_state is not None:
        return jsonify(object_state.to_dict())
    else:
        abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_obj(state_id):
    """Deletes a State object"""
    object_state = storage.get("State", state_id)
    if object_state is not None:
        storage.delete(object_state)
        storage.save()
        return jsonify({})
    else:
        abort(404)
    
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_obj():
    """Create a State object"""
    object_state = request.get_json()
    if 'name' not in object_state:
        return jsonify("Missing name"), 400
    elif object_state is not None:
        new = State(**object_state)
        new.save()
        return jsonify(new.to_dict()), 201
    else:
        return jsonify("Not a JSON"), 400

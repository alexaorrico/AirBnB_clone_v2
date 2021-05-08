#!/usr/bin/python3
""" States """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State



@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects: GET /api/v1/states"""
    dict_state = storage.all("State")
    my_list = []
    for value in dict_state.values():
        my_list.append(value.to_dict())

    return jsonify(my_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def object_state(state_id=None):
    """Retrieves a State object"""

    object_state = storage.get("State", state_id)
    if object_state is not None:
        return jsonify(object_state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_obj(state_id=None):
    """Deletes a State object"""
    object_state = storage.get("State", state_id)
    if object_state is not None:
        storage.delete(object_state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_obj():
    """Create a State object"""
    object_state = request.get_json(silent=True)
    if 'name' not in object_state.keys():
        abort(400, "Missing name")
    elif object_state is not None:
        new_o = State(**object_state)
        storage.new(new_o)
        new.save()
        return jsonify(new_o.to_dict()), 201
    else:
        abort(400, "Not a JSON")

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update(state_id=None):
    """ Update state """
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    req = request.get_json(silent=True)
    if req is None:
        abort(400, "Not a JSON")
    else:
        for key, value in s.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(obj, k, v)
        storage.save()
        final = obj.to_dict()
        return jsonify(final), 200

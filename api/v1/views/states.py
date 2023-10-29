#!/usr/bin/python3

"""
a view for State objects that handles all default RESTFul API actions

Author: Khotso Selading and Londeka Dlamini
"""


from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, make_response, request


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states():
    """Retrieves of a list of all state objects"""
    state_objects = storage.all(State)
    return jsonify([obj.to_dict() for obj in state_objects.values()])


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """retrieves specific state obj"""
    state_objects = storage.get(State, state_id)

    if not state_objects:
        abort(404)

    return jsonify(state_objects.to_dict())


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_state(state_id):
    """deletes specific state object"""
    state_objects = storage.get(State, state_id)

    if not state_objects:
        abort(404)

    state_objects.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
    """adds new state object to filestorage/database"""
    new_state_obj = request.get_json()

    if not new_state_obj:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if new_state_obj.get('name') is None:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_state = State(**new_state_obj)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def put_state(state_id):
    """adds new state object to filestorage/database"""
    state_object = storage.get(State, state_id)
    new_state_object = request.get_json()

    if not state_object:
        abort(404)
    if new_state_object is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in new_state_object.items():
        if key not in {'id', 'created_at', 'updated_at'}:
            setattr(state_object, key, value)

    state_object.save()
    return make_response(jsonify(state_object.to_dict()), 200)

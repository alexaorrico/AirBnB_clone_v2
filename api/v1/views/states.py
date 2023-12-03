#!/usr/bin/python3
"""State module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from flasgger.utils import swag_from


# GET
@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get.yml', methods=['GET'])
def get_states():
    """Retrieves the list of all State objects"""
    all_states = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(all_states)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/state/get_id.yml', methods=['GET'])
def get_state(state_id):
    """Retrieves a State object by id"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    return jsonify(state.to_dict())


# DELETE
@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/state/delete.yml', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State objct by id"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    state.delete()
    storage.save()
    return jsonify({})


# POST
@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/state/post.yml', methods=['POST'])
def create_state():
    """Creates a new State object"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    json_obj = request.get_json()
    obj = State(**json_obj)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


# PUT
@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/state/put.yml', methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get(State, state_id)

    if obj is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)

    storage.save()
    return jsonify(obj.to_dict())

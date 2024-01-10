#!/usr/bin/python3
"""State blueprint"""
from models import storage
from flask import jsonify, abort, make_request, request
from api.v1.views import app_views
from flasgger.utils import swag_from
from models.state import State


@app_views.route('/states', methods['GET'])
@swag_from('documentation/state/get.yml', methods=['GET'])
def get_all():
    '''Get all state by id'''
    state_list = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods['GET'])
@swag_from('documentation/state/get_id.yml', methods=['GET'])
def get_by_id(state_id):
    """Get state by id"""
    state_data = storage.get(State, state_id)
    if state_data is None:
        abort(404)
    return jsonify(state_data.to_dict())


@app_views.route('/states/<state_id>', methods['DELETE'])
@swag_from('documentation/state/delete.yml', methods=['DELETE'])
def delete_state(state_id):
    """Delete state by id"""
    state_data = storage.get(State, state_id)
    if state_data is None:
        abort(404)
    state_data.delete()
    state_data.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/state/post.yml', methods=['POST'])
def crete_state():
    """Create ne instance"""
    if not request.get_json():
        return make_request(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_request(jsonify({"error": "Missing name"}), 400)
    obj = State(request.get_json())
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/state/put.yml', methods=['PUT'])
def post_method(state_id):
    """ post method """
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

#!/usr/bin/python3
"""State module """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'])
def get_all():
    """gets all objects by id"""
    all_obj = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(all_obj)


@app_views.route('/states/<string:state_id>', methods=['GET'])
def get_method_state(state_id):
    """gets state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def del_method_state(state_id):
    """deletes state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'])
def create_state():
    """creates a state"""
    if not request.get_json():
        return make_reponse(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_reposnse(jsonify({"error": "Missing name"}), 400)
    state_js = request.get_json()
    obj = State(state_js)
    obj.save()
    return jsonify(obj.to_dict(), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def update_method(state_id):
    """updates states method"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict(), 200)

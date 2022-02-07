#!/usr/bin/python3
"""view for State objs that handles default RESTful API actions"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import State
from models import storage


obj_dict = storage.all('State')


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_state():
    """retrieves a list of all State objects"""
    return jsonify([obj.to_dict() for obj in obj_dict.values()])


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def get_state_obj(state_id):
    """gets State obj based on id, else None if not found"""
    state_obj = storage.get('State', state_id)
    if request.method == 'DELETE':
        if state_obj:
            state_obj.delete()
            storage.save()
        return jsonify({}), 200 if state_obj else abort(404)
    return jsonify(state_obj.to_dict()) if state_obj else abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates a state obj"""
    state_obj = storage.get('State', state_id)
    if not state_obj:
        abort(404)
    content = request.get_json()
    if not content:
        return jsonify('Not a JSON'), 400
    for key, val in content.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at':
            setattr(state_obj, key, val)
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a state"""
    content = request.get_json()
    if not content:
        return jsonify('Not a JSON'), 400
    if 'name' not in content:
        return jsonify('Missing name'), 400
    new_state = State(**content)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201                                                

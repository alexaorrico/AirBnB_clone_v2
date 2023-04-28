#!/usr/bin/python3
'''
API for State
'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
import models


@app_views.route('/states/', methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def all_states(state_id=None):
    '''Returns all states object in json format'''
    json_list = []
    try:
        if state_id is None:
            for v in storage.all('State').values():
                json_list.append(v.to_dict())
        else:
            json_list = storage.get('State', state_id).to_dict()
        return jsonify(json_list)
    except Exception:
        abort(404)


def attrib_update(obj, **args):
    '''Helper function to update objects attributes to correct types'''
    for key, value in args.items():
        if key not in ['id', 'created_at', 'updated_at'] and hasattr(obj, key):
            if isinstance(value, str):
                value = value.replace("_", " ")
            setattr(obj, key, value)


@app_views.route('/states/', methods=['POST'])
def create_state():
    '''Creates an instance of State and save it to storage'''
    form = request.get_json(force=True)
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    state_class = models.classes['State']
    new_state = state_class()
    attrib_update(new_state, **form)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    '''Deletes a state object'''
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)
    else:
        storage.delete(state_obj)
        storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    '''Updates State object attribute'''
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)
    form = request.get_json(force=True)
    attrib_update(state_obj, **form)
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200

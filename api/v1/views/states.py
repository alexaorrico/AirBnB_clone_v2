#!/usr/bin/python3
'''routes'''
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
import json


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''returns json to the route'''
    obj = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(obj)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states_id(state_id):
    '''return by id'''
    st = storage.get(State, state_id)

    if st is None:
        abort(404)
    st = st.to_dict()

    return jsonify(st)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_by_id(state_id):
    '''delete by id'''
    st = storage.get(State, state_id)
    if st is None:
        abort(404)
    st.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    '''creates a State obj'''
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({"error":  "Not a JSON"}), 400)
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    create = State(**data)

    create.save()
    create = create.to_dict()

    return jsonify(create), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    '''update state by id'''
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({"Not a JSON"}), 400)

    stat = storage.get(State, state_id)

    if stat is None:
        abort(404)
    for key, value in data.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            continue
        setattr(stat, key, value)
    storage.save()
    stat = stat.to_dict()

    return jsonify(stat), 200

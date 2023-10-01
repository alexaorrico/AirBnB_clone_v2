#!/usr/bin/python3

from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views, State, stoarge


def to_dict():
    """ retrieve an object into a valid JSON"""
    return jsonify({})

@app_views.route('/app/v1/states', method=['GET'])
def state_list():
    """ retrieve all list """
    for state in stoarge.all("State").values():
        all_states = state.to_json() 
    return jsonify({all_states})


@app_views.route('/app/v1/states/<state_id>', method=['GET'])
def state_object(state_id =None):
    """ retrieve all state object """
    if state_id is None:
        abort(404)
    state = stoarge.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_json())

@app_views.route('/app/v1/states/<state_id>', method=['DELETE'])
def state_delete(state_id =None):
    """ delete all state object """
    if state_id is None:
        abort(404)
    state = stoarge.get("State", state_id)
    if state is None:
        abort(404)
    stoarge.delete(state)
    return jsonify({}), 200

@app_views.route('/app/v1/states', method=['POST'])
def state_create():
    """ create all state object """
    data = None
    try:
        data = request.get_json()
    except:
        data = None
    if data is None:
        return jsonify({"Not a JSON"}), 400
    if 'name' not in data.keys():
        return jsonify({"Missing name"}), 400
    state = State(**data)
    state.save()
    return jsonify(state.to_json()), 201


@app_views.route('/app/v1/states/<state_id>', method=['PUT'])
def state_update(state_id = None):
    """ update all state object """
    data = None
    try:
        data = request.get_json()
    except:
        data = None
    if data is None:
        return jsonify({"Not a JSON"}), 400
    state = stoarge.get("State", state_id)
    if state is None:
        abort(404)
    for keys, values in data.items():
        if keys not in ('id', 'created_at', 'updated_at'):
            setattr(state, keys, values)
    state.save()
    return jsonify(state.to_json()), 200



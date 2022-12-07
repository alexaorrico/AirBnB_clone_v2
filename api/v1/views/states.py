#!/usr/bin/python3
"""
index
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage 
from models.state import State

@app_views.route('/states', methods=['GET'])
def get_states():
    """ Get All States"""
    states = storage.all(State).values()

    return jsonify([state.to_dict() for state in states ])

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ Get State with Id"""
    state = storage.get(State, state_id) 
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ DELETE State With id"""
    state = storage.get(State, state_id) 
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()

    return jsonify({}), 200

@app_views.route('/states', methods=['POST'])
def post_state():
    """ Post State """
    try:
        body = request.get_json(force=True)
    
        if  body is None:
            abort(400, description="Not a JSON")
        elif body.get('name') is None:
            abort(400, description= 'Missing name')    
        else:
            obj = State(**body)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    except ValueError:
        abort(400, desciption="Not a JSON")

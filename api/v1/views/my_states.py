#!/usr/bin/python3
"""
This file contains the Review module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request as req, make_response as mr
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State


# GET '/api/v1/states' RESTful API endpoint
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get the states from storage"""
    states = storage.all(State).values()
    # jsonify list of dicts of state objs and return
    return mr(jsonify([state.to_dict() for state in states]), 200)


# GET '/api/v1/states/<state_id>' RESTful API endpoint
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """get the states by id from storage"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return mr(jsonify(state.to_dict()), 200)


# DELETE '/api/v1/states/<state_id>' RESTful API endpoint
@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """delete a state by id from storage"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return mr(jsonify({}), 200)


# POST '/api/v1/states' RESTful API endpoint
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """post a new state to storage"""
    if req.json:
        if 'name' in req.json:
            data = req.get_json()
            new_state = State(**data)
            storage.new(new_state)
            storage.save()
            return mr(jsonify(new_state.to_dict()), 201)
        elif 'states' in req.json:
            data = req.get_json()
            new_states = data.get('states', [])
            for state in new_states:
                new_state = State(**state)
                storage.new(new_state)
                storage.save()
            return mr(jsonify([s for s in new_states]), 201)
        else:
            abort(400, description='Missing name')
    abort(400, description='Not a JSON')


# PUT '/api/v1/states/<state_id>' RESTful API endpoint
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_by_id(state_id):
    """update an existing state on storage"""
    ignore = ['id', 'created_at', 'updated_at']
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if req.json and isinstance(req.json, dict):
        data = req.get_json()
        for key, value in data.items():
            if key in ignore:
                pass
            else:
                state = storage.get(State, state_id)
                setattr(state, key, value)
                storage.save()
            return mr(jsonify(state.to_dict()), 200)
    else:
        abort(400, description="Not a JSON")

#!/usr/bin/python3
"""states routes module"""
from api.v1.views import app_views
from api.v1.views import *
from models import storage
from flask import jsonify, make_response, abort, request
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def states(state_id=None):
    """[GET] Retrieves a list of all State objects"""
    if not state_id:
        objs = [obj.to_dict() for obj in storage.all('State').values()]
        return jsonify(objs)
    return retrieve_model('State', state_id)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_state(state_id):
    """[DELETE] - deletes a state object with specified id"""
    return del_model('State', state_id)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """[POST] - adds a state object"""
    data = {'name'}
    return create_model('State', None, None, data)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """[PUT] - updates a state object"""
    auto_data = ['id', 'created_at', 'updated_at']
    return update_model('State', state_id, auto_data)

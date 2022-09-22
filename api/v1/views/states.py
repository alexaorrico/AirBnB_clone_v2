#!/usr/bin/python3
"""
flask application module for retrieval of
State Objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.exceptions import *
from models.state import State


@app_views.route('/states',
                 methods=['GET'],
                 strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects"""
    return (jsonify(State.api_get_all()), 200)


@app_views.route('/states',
                 methods=['POST'],
                 strict_slashes=False)
def post_states():
    """Creates a State"""
    try:
        return (jsonify(
            State.api_post(
                request.get_json(silent=True))),
                201)
    except BaseModelMissingAttribute as attr:
        return (jsonify({'error': 'Missing {}'.format(attr)}), 400)
    except BaseModelInvalidDataDictionary:
        return (jsonify({'error': "Not a JSON"}), 400)

@app_views.route('/states/<string:state_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    """handles get State object: state_id"""
    try:
        return (jsonify(
            State.api_get_single(state_id)), 200)
    except BaseModelInvalidObject:
        abort(404)

@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """handles State object: state_id"""
    try:
        return (jsonify(
            State.api_delete(state_id)), 200)
    except BaseModelInvalidObject:
        abort(404)

@app_views.route('/states/<string:state_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_state_by_id(state_id):
    """handles update of State object: state_id"""
    try:
        return(State.api_put(
                request.get_json(silent=True),
                state_id),
                200)
    except BaseModelInvalidDataDictionary:
        return (jsonify({'error': "Not a JSON"}), 400)
    except BaseModelInvalidObject:
        abort(404)
    

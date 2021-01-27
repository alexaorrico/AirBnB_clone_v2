#!/usr/bin/python3
"""
 New view for State objects that handles all default RestFul API actions.
"""
from models import BaseModel, State, storage
from flask import Flask, request, jasonify
from api.v1.views import app_views


@app_views.route('/api/v1/states', methods=['GET'])
def all_states():
    """ Retrieves the list of all State objects. """
    list_of_states = []
    for value in storage.all('State').values():
        list_of_states.append(value.to_dict())
    return jsonify(list_of_states)


@app_views.route('/api/v1/states/<state_id>', methods=['GET'])
def specific_state(state_id):
    """ Retrieves a State object. """


@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object. """


@app_views.route('/api/v1/states', methods=['POST'])
def create_state():
    """ Creates a State. """


@app_views.route('/api/v1/states/<state_id>', methods=['PUT'])
def updates_state(state_id):
    """ Updates a State object. """

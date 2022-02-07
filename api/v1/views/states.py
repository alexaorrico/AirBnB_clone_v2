#!/usr/bin/python3
"""states"""

from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import Flask, jsonify, abort, request, make_response


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def states():
    """ list obj """
    if request.method == 'GET':
        states = []
        for state in storage.all(State).values():
            states.append(state.to_dict())
        return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getState(state_id):
    """retrieves state obk"""
    if request.method == 'GET':
        if storage.get(State, state_id) is not None:
            return jsonify(storage.get(State, state_id).to_dict())
        abort(404)

@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def deleteState(state_id):
    """ deletea State object """
    if request.method == 'DELETE':
        if storage.get(State, state_id) is not None:
            storage.delete(storage.get(State, state_id))
            storage.save()

            return jsonify({}), 200
        abort(404)

@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def createState():
    """ creates State"""
    if request.method == 'POST':
        r = request.headers.get('Content-Type')
        if r != 'application/json':
            return jsonify('Not a JSON'), 400
        rn = request.get_json()
        if 'name' not in rn:
            return jsonify('Missing name'), 400
        ns = State(**rn)
        ns.save()
        return jsonify(ns.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates state """
    if request.method == 'PUT':

        r = request.headers.get('Content-Type')

        if r != 'application/json':
            return jsonify('Not a JSON'), 400

        ur = request.get_json()

        if storage.get(State, state_id) is not None:

            if 'name' in ur:
                storage.get(State, state_id).name = upr['name']
                storage.get(State, state_id).save()

                return jsonify(storage.get(State, state_id).to_dict()), 200
        abort(404)                                    

#!/usr/bin/python3
""" Your first endpoint (route) will be to return the status of your API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
import json

@app_views.route('/states/', methods=['GET'])
def show_states():
    """ returns list of states """
    lista = []
    states = storage.all(State).values()
    for state in states:
        lista.append(state.to_dict())
    return jsonify(lista)

@app_views.route('states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def show_state(state_id):
    """ returns state data """
    if request.method == 'GET':
        states = storage.all(State).values()
        for state in states:
            if state.id == state_id:
                return jsonify(state.to_dict())
        abort(404)
    elif request.method == 'DELETE':
        states = storage.all(State).values()
        for state in states:
            if state.id == state_id:
                state.delete()
                storage.save()
                return jsonify({}), 200
        abort(404)

@app_views.route('/states/', methods=['POST'])
def create_state():
    """ create state """
    if request.json:
        new_dict = request.get_json()
        if "name" in new_dict.keys():
            new_state = State(**new_dict)
            storage.new(new_state)
            storage.save()
            return jsonify(new_state.to_dict()), 201
        else:
            abort(400, description="Missing name")
    else:
        abort(400, desciption="Not a JSON")

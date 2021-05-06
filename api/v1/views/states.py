#!/usr/bin/python3
""" Your first endpoint (route) will be to return the status of your API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
import json

@app_views.route('/states/', methods=['GET',])
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

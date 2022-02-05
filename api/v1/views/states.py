#!/usr/bin/python3
""" states routes """
from api.v1.views import app_views
from flask import Flask, jsonify, abort
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def states():
    """ list of states """
    states = storage.all('State')
    return jsonify([value.to_dict() for value in states.values()])


@app_views.route('/states/<string:id>', strict_slashes=False)
def state_id(id):
    """ json data of a sngle state """
    single_state = (storage.get(State, id))
    if single_state:
        return jsonify(single_state.to_dict()), 200
    abort(404)

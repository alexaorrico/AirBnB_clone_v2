#!/usr/bin/python3
""" New view for Stat objects that handles default API actions """

from flask import Flask, Blueprint, jsonify, request, url_for, abort
from models.base_model import BaseModel
from api.v1.views import app_views
from models import storage
from models.state import State
import json


@app_views.route("/states/<string:state_id>", methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """ shows specific class with given id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """ by default, shows all states """
    states = storage.all(State).values()
    new_list = []
    for state in states:
        new_list.append(state.to_dict())
    return jsonify(new_list)


@app_views.route("/states/<string:state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ deletes the class associated with given id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'],
                 strict_slashes=False)
def post_state():
    """ creates something new with parameters """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT', 'GET'],
                 strict_slashes=False)
def put_state(state_id):
    """ updates class with information """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.is_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(state, attr, val)
    state.save()
    return jsonify(state.to_dict()), 200

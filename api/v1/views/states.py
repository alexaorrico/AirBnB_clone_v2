#!/usr/bin/python3
"""
script that starts a Flask web application:
"""
from os import error, getenv
from models import storage
from api.v1.views import app_views
from flask import Blueprint, render_template, abort
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/api/v1/states', methods=['GET'])
def state():
    """
    Retrieves the list of all State objects
    """
    list = []
    for state in storage.all["State"].values():
        list.append(state.to_dict)
    return jsonify(list)


@app.route('/api/v1/states/<state_id>', methods=['GET'])
def state_get(state_id):
    """
    Retrieves a State object:
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    else:
        return state.to_dict()


@app.route('/api/v1/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    """
    Deletes a State object
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 202


@app.route('/api/v1/states', methods=['POST'])
def state_post():
    """
    Creates a State
    """
    state = request.get_json()
    if state is None:
        abort(404, "Not a JSON")

    if 'name' not in state:
        abort(404, "Missing name")
    else:
        new = state.State(**state)
        storage.new(new)
        storage.save()
        return jsonify(new.to_dict()), 201


@app.route('/api/v1/states/<state_id>', methods=['PUT'])
def state_put(state_id):
    """
    Updates a State object
    """
    state = request.get_json()
    if state is None:
        abort(404, "Not a JSON")

    if 'name' not in state:
        abort(404, "Missing name")
    else:
        state.save()
        state.new()
        return (jsonify(state), 201)

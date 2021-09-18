#!/usr/bin/python3
"""
script that starts a Flask web application:
"""
from os import error, getenv
from models import storage
from api.v1.views import app_views
from flask import Blueprint, render_template, abort
from flask import Flask, jsonify, Response, make_response

app = Flask(__name__)


@app.route('/api/v1/states', methods=['GET'])
def state():
    list = []
    for state in storage.all["State"].values():
        list.append(state.to_dict)
    return jsonify(list)


@app.route('/api/v1/states/<state_id>', methods=['GET'])
def state_get(state_id):
    list = []
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    return state.to_dict()


@app.route('/api/v1/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    empy = {}
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    state.delete()
    state.save()
    return jsonify({}), 202


@app.route('/api/v1/states', methods=['POST'])
def state_post():
    state = request.get_json()
    if state is None:
        abort(404, "Not a JSON")

    if 'name' not in state:
        abort(404, "Missing name")
    else:
        state.save()
        state.new()
        return (jsonify(state), 201)


@app.route('/api/v1/states/<state_id>', methods=['PUT'])
def state_put(state_id):
    state = request.get_json()
    if state is None:
        abort(404, "Not a JSON")

    if 'name' not in state:
        abort(404, "Missing name")
    else:
        state.save()
        state.new()
        return (jsonify(state), 201)

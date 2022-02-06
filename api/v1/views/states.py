#!/usr/bin/python3
"""state"""

from ast import Delete
from crypt import methods
from pickle import GET, PUT
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models.state import State


@app_views.route("/states", methods=["GET"])
def state():
    """state"""
    lists = []
    j = storage.all('State').values()
    for i in j:
        lists.append(i.to_dict())
    return jsonify(lists)


@app_views.route("/states/<id>", methods=["GET"])
def stateid(id):
    """id retrieve json object"""
    j = storage.all('State').values()
    for i in j:
        if i.id == id:
            return jsonify(i.to_dict())
    abort(404)


@app_views.route("/states/<id>", methods=["DELETE"])
def state_del(id):
    """delete state with id"""
    state = storage.get('State', id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<id>", methods=["POST"])
def state_post(id):
    """create new state"""
    date = request.get_json()
    if not date:
        abort(400, "Not a JSON")
    if 'name' not in date.keys():
        abort(400, "Missing name")
    new_date = State(**date)
    storage.save()
    return make_response(jsonify(new_date.to_dict()), 201)


@app_views.route("/states/<id>", methods=["PUT"])
def state_put(id):
    """update a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(400)
    if not request.get_json():
        abort(400, "Not a JSON")
    dat = request.get_json()
    Ignore = ['id', 'created_at', 'updated_at']
    for key, value in dat.items():
        if key not in Ignore:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)

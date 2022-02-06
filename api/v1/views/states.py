#!/usr/bin/python3
"""state"""

from ast import Delete
from crypt import methods
from pickle import GET, PUT
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
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
    state = storage.get('State', id )
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<id>", methods=["POST"])
def state_post(id):
    """create new state"""
    date = request.get_json()
    if date is None:
        abort(400, "Not a JSON")
    if not date.get('name'):
        abort(400, "Missing name")
    new_date = State(**date)
    storage.new(new_date)
    storage.save()
    return jsonify(new_date.to_dict()), 201


@app_views.route("/states/<id>", methods=["PUT"])
def state_put(id):
    """update a state object"""
    dat = request.get_json()
    if dat is None:
        abort(400, "Not a JSON")
    Ignore = ['id', 'created_at', 'updated_at']
    state = storage.get("State", id)
    if state is None:
        abort(404)
    for x, y in dat.items():
        if x not in Ignore:
            setattr(state, x, y)
    state.save()
    return jsonify(state.to_dict()), 200


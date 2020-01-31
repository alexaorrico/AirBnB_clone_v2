#!/usr/bin/python3
"""
    state endpoint
"""
from flask import Flask, abort, jsonify, request
from api.v1.views import app_views
from models.state import State
from models import storage


def get_state(state):
    """ get """
    if state:
        (jsonify(state.to_dict()), 200)
    return abort(404)


def put_state(state):
    """ put """
    if not state:
        abort(404)
    try:
        x = request.get_json()
    except:
        abort(400, "Not a JSON")
    for key in new:
        if key not in ("id", "created_at", "updated_at"):
            setattr(state, key, new[key])
    storage.save()
    return (jsonify(state.to_dict()), 200)


def delete_state(state):
    """ delete """
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return (jsonify(dict()), 200)


methods = {
    "GET": get_state,
    "PUT": put_state,
    "DELETE": delete_state,
}


@app_views.route("/states", methods=["GET", "POST"])
def states():
    """ list or create """
    if request.method == "GET":
        return (jsonify([
            s.to_dict()
            for s
            in storage.all("State").values()
        ]), 200)
    elif request.method == "POST":
        try:
            data = request.get_json()
        except:
            abort(400, "Not a JSON")
        if "name" not in data:
            abort(400, "Missing name")
        new = State(data)
        new.save()
        return (jsonify(new.to_dict()), 201)


@app_views.route("/states/<id>", methods=["GET", "PUT", "DELETE"])
def states_id(id):
    """ states """
    for state in storage.all("State").values():
        if state.id == id and request.method in methods:
            return methods[request.method](state)
    abort(404, "Not found")

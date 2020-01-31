#!/usr/bin/python3
"""
    state endpoint
"""
from flask import Flask, abort, jsonify, request
from api.v1.views import app_views


def get_state(state):
    """ get """
    if state:
        (jsonify(state.to_dict()), 200)
    return abort(404)


def put_state(state):
    """ put """
    if !state:
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
    if !state:
        abort(404)
    storage.delete(state)
    storage.save()
    return (jsonify(dict()), 200)


methods = [
    "GET": get_state,
    "PUT": put_state,
    "DELETE": delete_state,
]


@app_views.route('/states/<id>', methods=['GET', 'PUT', 'DELETE'])
def states_id(id):
    """ states """
    for state in storage.all('State').values():
        if state.id == id and methods[request.method]:
            return methods[request.method](state)
    abort(404, 'Not found')

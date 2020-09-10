#!/usr/bin/python3
"""new view for State objects"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route(
    '/states',
    methods=['GET', 'POST'],
    strict_slashes=False
)
def states():
    """ GET and POST   """

    if request.method == "GET":
        states = [state.to_dict() for state in storage.all('State').values()]
        return jsonify(list(states))

    if request.method == "POST":
        jreq = request.get_json()
        if jreq is None:
            abort(400, 'Not a JSON')

        if 'name' not in jreq.keys():
            abort(400, 'Missing name')

        state = State(**jreq)
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route(
    '/states/<state_id>',
    methods=['GET', 'DELETE', 'PUT'],
    strict_slashes=False
)
def state(state_id):
    """ GET, DELETE, and PUT """

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == "GET":
        return jsonify(state.to_dict())

    if request.method == "DELETE":
        state.delete()
        storage.save()
        return jsonify({})

    if request.method == "PUT":
        jreq = request.get_json()
        if jreq is None:
            abort(400, 'Not a JSON')

        for k, v in jreq.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(state, k, v)
        state.save()
        return jsonify(state.to_dict())

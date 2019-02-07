#!/usr/bin/python3
""" prepares data for easier viewing """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import OperationalError


@app_views.route('/states', methods=['GET'])
def get_all_states():
    """ Returns all the state obj in json """
    states = storage.all(State).values()
    states = [state.to_dict() for state in states]
    return jsonify(states)


@app_views.route('/states', methods=['POST'])
@app_views.route('/states/<state_id>', methods=['DELETE', 'GET', 'PUT'])
def get_put_delete_state(state_id=None):
    """ gets or deletes state from storage """
    if state_id:
        state = storage.get('State', state_id)
    else:
        state = None

    if not state and request.method != 'POST':
        abort(404)

    if request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({})

    if request.method != 'GET':
        """ handles put and post """
        if request.mimetype != 'application/json':
            return jsonify(error="Not a JSON"), 400
        try:
            state_json = request.get_json()
        except BadRequest:
            return jsonify(error="Not a JSON"), 400

        if request.method == 'PUT':
            if state_json.get('id'):
                state_json.pop('id')
            if state_json.get('created_at'):
                state_json.pop('created_at')
            if state_json.get('updated_at'):
                state_json.pop('updated_at')
            for k, v in state_json.items():
                setattr(state, k, v)
                state.save()

        if request.method == 'POST':
            state = State(**state_json)
            try:
                state.save()
            except OperationalError:
                return jsonify(error="Missing name"), 400
            return jsonify(state.to_dict()), 201

    return jsonify(state.to_dict())

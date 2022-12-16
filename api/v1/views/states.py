#!/usr/bin/python3
""" new view for State objects """

from models import storage
from api.v1.views import app_views
from models.state import State
from flask import Flask, make_response, jsonify
import requests
from flask import request

meths = ['GET', 'DELATE', 'POST', 'PUT']

@app_views.route('/states', methods=meths, strict_slashes=False)
@app_views.route('/states/<state_id>')
def get_states(state_id=None):
    """ Retrieves the list of all State objects """
    if state_id is not None:
        if request.method == 'GET':
            """ Method GET """ 
            obj = storage.get(State, state_id)
            if obj is None:
                return make_response(jsonify({'error': 'Not found'}), 404)
            else:
                return obj.to_dict()

        if request.method == 'DELETE':
            """ Method DELETE """
            obj = storage.get(State, state_id)
            if obj is None:
                return make_response(jsonify({'error': 'Not found'}), 404)
            else:
                key = "{}.{}".format(State.__name__, state_id)
                storage.delete(obj)
                storage.save()
                if key not in storage.all():
                    return make_response('{}', 200)

    else:
        if request.method == 'GET':
                """ Method GET """ 
                state_objs = [state.to_dict() for state in storage.all(State).values()]
                return state_objs

        if request.method == 'POST':
            data = request.get_json(silent=True, force=True)
            if data is None:
                return make_response(jsonify({'error': 'Not a JSON'}), 404)
            else:
                if 'name' not in data:
                    return make_response(jsonify({'error': 'Missing name'}), 404)

            obj = State(**data)
            obj.save()
            return make_response(jsonify(obj.to_dict()), 201)

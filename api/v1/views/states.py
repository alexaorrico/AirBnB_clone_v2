#!/usr/bin/python3
""" new view for State objects """

from models import storage
from api.v1.views import app_views
from models.state import State
from flask import Flask, make_response, jsonify
import requests
from flask import request

meths = ['GET', 'DELETE', 'POST', 'PUT']

@app_views.route('/states', methods=meths, strict_slashes=False)
@app_views.route('/states/<state_id>')
def get_states(state_id=None):
    """ Retrieves the list of all State objects """
    if request.method == 'GET':
        """ Method GET """ 
        if state_id is None:
            state_objs = [state.to_dict() for state in storage.all(State).values()]
            return state_objs
        else:
            obj = storage.get(State, state_id)
            if obj is None:
                return make_response(jsonify({'error': 'Not found'}), 404)
            else:
                return obj.to_dict()
    
    if request.method == 'PUT':
        if state_id is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 404)
        else:
            obj = storage.get(State, state_id)
            if obj is None:
                return make_response(jsonify({'error': 'Not found'}), 404)
            else:
                data = request.get_json()
                if data is None:
                    return make_response(jsonify({'error': 'Not a JSON'}), 404)
                else:
                    [setattr(obj, **data) for item in data if item != ('id', 'created_at', 'updated_at')]
                    obj.save()
                    return make_response(jsonify(obj), 200)

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
            return make_response(jsonify('{}'), 200)

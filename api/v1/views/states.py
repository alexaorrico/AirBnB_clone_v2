#!/usr/bin/python3
''' new view for State objects'''

from flask import Flask
from flask import Flask, abort
from api.v1.views import app_views
from os import name
from models.state import State
from flask import request


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def toGet():
    '''getting thing'''
    objects = storage.all('State')
    lista = []
    for state in objects.values():
        lista.append(state.to_dict())
    return jsonify(lista)


@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def toGetid(state_id):
    '''Retrieves a State object id'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def posting():
    '''Creates a State'''
    response = request.get_json()
    if response is None:
        abort(400, {'Not a JSON'})
    if "name" not in response:
        abort(400, {'Missing name'})
    state = State(name=response['name'])
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def putinV(state_id):
    '''vladimir'''
    response = request.get_json()
    if response is None:
        abort(400, {'Not a JSON'})
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in response.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<string:state_id>', methods=['DELETE'], strict_slashes=False)
def deleting(state_id):
    ''' to delete an onbject'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

#!/usr/bin/python3
''' new view for State objects'''

from flask import Flask
from flask import Flask, abort
from api.v1.views import app_views
from os import name
from models.state import State
from flask import request


@app_views.route('/status', methods=['GET'] strict_slashes=False)
def toGet():
    '''getting thing'''
    objects = storage.all('State')
    lista = []
    for state in objects.values():
        lista.append(state.to_dict())
    return jsonify(lista)


@app_views.route('/states/<string:stateid>', methods=['GET'],
                 strict_slashes=False)
def toGetid():
    '''Updates a State object id'''
    objects = storage.get('State', 'state_id')
    if objects is None:
        abort(404)
    return jsonify(objects.to_dict()), 'OK'


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def posting():
    '''Creates a State'''
    response = request.get_json()
    if response id None:
        abort(400, {'Not a JSON'})
    if "name" not in response:
        abort(400, {'Missing name'})
    stateObject = State(name=response['name'])
    storage.new(stateObject)
    storage.save()
    return jsonify(stateObject.to_dict()), '201'


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def putinV():
    '''vladimir'''
    response = request.get_json()
    if response id None:
        abort(400, {'Not a JSON'})
    stateObject = storage.get(State, state_id)
    if stateObject is None:
        abort(404)
    ignoreKeys = ['id', 'created_at', 'updated_at']
    for key in response.items():
        if key not in ignoreKeys:
            setattr(stateObject, key)
    storage.save()
    return jsonify(stateObject.to_dict()), '200'


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleting():
    ''' to delete an onbject'''
    stateObject = storage.get(State, state_id)
    if stateObject is None:
        abort(404)
    storage.delete(stateObject)
    storage.save()
    return jsonify({}), '200'

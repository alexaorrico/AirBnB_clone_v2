#!/usr/bin/python3
"""function to create the route status"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.state import State


@app_views.route('/states')
def states():
    states = []
    for val in storage.all("State").values():
        states.append(val.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>')
def states_id(state_id):
    for val in storage.all("State").values():
        if val.id == state_id:
            return jsonify(val.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def states_delete(state_id):
    states = storage.get("State", state_id)
    if states == None:
        abort(404)
    storage.delete(states)
    storage.save()
    storage.close()
    return jsonify({})


""" @app_views.route('/stats')
def stats():
    status render template for json
    dict_objs = {'amenities': 'Amenity', 'cities': 'City', 'places': 'Place',
                 'reviews': 'Review', 'states': 'State', 'users': 'User'}
    new_dict = {}
    for k, v in dict_objs.items():
        new_dict[k] = storage.count(v)
    return jsonify(new_dict) """

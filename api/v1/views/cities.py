#!/usr/bin/python3
"""view cities object"""

from sre_parse import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State

@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def cities_by_states(state_id):
    """return list of all object cities"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = list()
    list_cities = storage.all('City')
    for value in list_cities.values():
        if state_id == value.state_id:
            cities.append(value.to_dict())
    return jsonify(cities)


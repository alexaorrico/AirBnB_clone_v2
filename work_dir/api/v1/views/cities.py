#!/usr/bin/python3
"""
This module will help us control and manage state objects using Restful api
"""
from flask import request, abort, jsonify
from models.city import City
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def allCities_inState(state_id):
    """
    returns a list of all cities in a city
    """
    c_list = []
    state = storage.get(State, state_id)
    for city in state.cities:
        c_list.append(city)
        c_list = c_list.to_dict()
    return jsonify(c_list)

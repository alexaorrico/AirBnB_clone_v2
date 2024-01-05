#!/usr/bin/python3
"""view for City objects handles all
   default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """get all cities in a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = []
    for city in state.cities:
        data.append(city.to_dict())
    return jsonify(data)

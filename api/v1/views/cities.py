#!/usr/bin/python3
"""states script"""

from api.v1.views import app_views
from flask import jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def list_all_cities(state_id):
    '''Retrieves a list of all city objects of a state id'''
    state = storage.get(State, state_id)
    if state is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    list_cities = [city.to_dict() for city in state.cities]
    return jsonify(list_cities)

#!/usr/bin/python3
""" blablabla
"""
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify. abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Return list of cities in a state"""
    unique_state = storage.get("State", state_id)
    if not unique_state:
        abort(404)
    city_list = []
    for city in unique_state.cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)

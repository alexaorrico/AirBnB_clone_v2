#!/usr/bin/python3
"""handles all defaults RESTful API actions for cities"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.base_model import BaseModel


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """retrieves all cities of a given state"""
    from models import storage

    state = storage.get(State, state_id)
    if state:
        cities = storage.all(City)
        city_list = []

        for city in cities:
            if getattr(city, "state_id", "") == state_id:
                city_list.append(city.to_dict())
        return jsonify(city_list)
    return abort(404)

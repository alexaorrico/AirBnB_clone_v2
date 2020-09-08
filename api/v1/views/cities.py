#!/usr/bin/python3
"""VIew for States"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.city import City
from flask import abort
from flask import make_response
from flask import request
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['GET'])
def get_cities(state_id):
    """Return cities according to id of state object
        or return Error: Not found if it doesn't exist.
    """
    if state_id:
        dict_state = storage.get(State, state_id)
        if dict_state is None:
            abort(404)
        else:
            cities = storage.all(City).values()
            list_cities = []
            for city in cities:
                if city.state_id == state_id:
                    list_cities.append(city.to_dict())
            return jsonify(list_cities)

#!/usr/bin/python3
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from app import not_found
from flask import jsonify

@app_views.route('/states/<state_id>/cities', method=['GET'])
def get_cities(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return not_found()
    else:
        cities = storage.all(City)
        filtered_cities = []
        for city in cities:
            if state_id == city["state_id"]:
                filtered_cities.append(city)
        return jsonify(filtered_cities)
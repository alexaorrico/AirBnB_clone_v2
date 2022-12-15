#!/usr/bin/python3
"""     """


from models import storage
from models.city import City
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/states/<string:state_id>/cities", methods=["GET"], strict_slashes=False)

def get_cities(state_id):
    if state_id is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'], strict_slashes=False)

def city(city_id):
    if city is None:
        abort(404)
    return jsonify(city.to_dict())
#!/usr/bin/python3
""" Import the app_views blueprint for cities API endpoints """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>/cities/', methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """ Get all cities objects """
    all_status = storage.all("State").values()
    state_objs = [state.to_dict() for state in all_status if state_id == state.id]
    if not state_objs:
        abort(404)
    all_cities = storage.all("City").values()
    list_cities = [city.to_dict() for city in all_cities if state_id == city.state_id]
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Get a city by id """
    all_cities = storage.all("City").values()
    list_city = [city.to_dict() for city in all_cities if city.id == city_id]
    if not list_city:
        abort(404)
    return jsonify(list_city[0])


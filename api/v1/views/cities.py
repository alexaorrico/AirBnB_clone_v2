#!/usr/bin/python3

from flask import abort, request, make_response, jsonify

from api.v1.views import app_views
from models import City, storage

@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False)
def get_city_for_state(state_id):
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return make_response(jsonify(cities), 200)

@app_views.route(
    '/cities/<city_id>',
    methods=['GET'],
    strict_slashes=False)
def get_city(city_id):
    city = storage.get('City', city_id)
    if state is None:
        abort(404)
    return make_response(jsonify(city.to_dict()), 200)

@app_views.route(
    '/cities/<city_id>',
    methods=['DELTE'],
    strict_slashes=False)
def delete_city(city_id):
    city = storage.get('City', city_id)
    if state is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route(
    '/cities/<city_id>',
    methods=['PUT'],
    strict_slashes=False)
def put_city(city_id):
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    city = storage.get('City', city_id)
    if state is None:
        abort(404)
    city_dict = request.get_json()
    city.name = city_dict['name']
    city.save()
    return make_response(jsonify(city.to_dict()), 200)

#!/usr/bin/python3
"""
City view for API.

"""

from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False)
def get_city_for_state(state_id):
    """Returns JSON cities in a given state"""
    state = storage.get('State', state_id)
    if state:
        cities = [city.to_dict() for city in state.cities]
        return (jsonify(cities), 200)
    abort(404)


@app_views.route(
    '/cities/<city_id>',
    methods=['GET'],
    strict_slashes=False)
def get_city(city_id):
    """Returns JSON city and id"""
    city = storage.get('City', city_id)
    if city:
        return (jsonify(city.to_dict()), 200)
    abort(404)


@app_views.route(
    '/cities/<city_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_city(city_id):
    """Deletes a city given the id"""
    city = storage.get('City', city_id)
    if city:
        city.delete()
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False)
def post_city(state_id):
    """Creates a city in a given state"""
    state = storage.get('State', state_id)
    city_dict = request.get_json()
    if not city_dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in city_dict:
        return (jsonify({'error': 'Missing name'}), 400)
    if state:
        city_dict['state_id'] = state.id
        city = City(**city_dict)
        city.save()
        return (jsonify(city.to_dict()), 201)
    abort(404)


@app_views.route(
    '/cities/<city_id>',
    methods=['PUT'],
    strict_slashes=False)
def put_city(city_id):
    """Updates an existing city"""
    city_dict = request.get_json()
    if not city_dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    city = storage.get('City', city_id)
    if city:
        city.name = city_dict['name']
        city.save()
        return (jsonify(city.to_dict()), 200)
    abort(404)

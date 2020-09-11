#!/usr/bin/python3
""" View for City objects that handles
    all default RestFul API actions
"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """ Retrieves the list of all City objects of a State:
        GET /api/v1/states/<state_id>/cities
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ Retrieves a City object. :
        GET /api/v1/cities/<city_id>
    """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object:
        DELETE /api/v1/cities/<city_id>
    """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/<state_id>/cities/',
                 methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ Creates a City:
        POST /api/v1/states/<state_id>/cities
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    kwargs = request.get_json()
    kwargs['state_id'] = state_id
    city = City(**kwargs)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """ Updates a City object:
        PUT /api/v1/cities/<city_id>
    """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        setattr(city, attr, val)
    city.save()
    return jsonify(city.to_dict())

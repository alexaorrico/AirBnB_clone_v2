#!/usr/bin/python3
""" City view """
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.state import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def list_cities(state_id):
    """ Retrieves the list of all City objects of a State """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    cities = []
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities(city_id):
    """ Retrieves a City object """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def cities_delete(city_id):
    """ Delete a City object """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def new_city(state_id):
    """ Creates a new City """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    new_city = request.get_json()
    if not new_city:
        abort(400, 'Not a JSON')
    if 'name' not in new_city:
        abort(400, 'Missing name')
    new_city['state_id'] = state_id
    city = City(**new_city)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_id_put(city_id):
    """ Updates a City object """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    request_json = request.get_json()
    if not request_json:
        abort(400, 'Not a JSON')
    for key, value in request_json.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)

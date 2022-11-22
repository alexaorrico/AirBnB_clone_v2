#!/usr/bin/python3
""" view for State objects that handles all default RESTFul API actions """
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route(
    '/states/<state_id>/cities', methods=['GET'],
    strict_slashes=False,
)
def getCities(state_id):
    """ Retrieves the list of all City objects of a State """
    state_obj = storage.get(State, state_id)
    if state_obj:
        cities_obj = [city.to_dict() for city in state_obj.cities]
        return (jsonify(cities_obj), 200)

    abort(404)


@app_views.route(
    '/cities/<city_id>', methods=['GET'],
    strict_slashes=False
)
def getCityById(city_id):
    """ Retrieves a City object by id """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    return (jsonify(obj.to_dict()), 200)


@app_views.route(
    '/cities/<city_id>', methods=['DELETE'],
    strict_slashes=False
)
def deleteCityById(city_id):
    """ Deletes City object by id """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def newCityState(state_id):
    """ Creates a city """
    state_obj = storage.get(State, state_id)
    city_dict = request.get_json()
    if not city_dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in city_dict:
        return (jsonify({'error': 'Missing name'}), 400)
    if state_obj is not None:
        city_dict['state_id'] = state_obj.id
        city = City(**city_dict)
        city.save()
        return (jsonify(city.to_dict()), 201)

    abort(404)


@app_views.route(
    '/cities/<city_id>', methods=['PUT'],
    strict_slashes=False
)
def updateCity(city_id):
    """ Update the City object """
    if not request.get_json():
        return (jsonify({'error': 'Not a JSON'}), 400)
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return (jsonify(obj.to_dict()))

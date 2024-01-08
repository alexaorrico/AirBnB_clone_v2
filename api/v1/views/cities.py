#!/usr/bin/python3
""" The module that includes the City View """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all City
    If the state_id is not linked to any State object, raise a 404 error
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities), 200


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def city(city_id):
    """
    Retrieves a City object based on `city_id`
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_removal(city_id):
    """
    Deletes a City object based on `city_id`.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def creation_city(state_id):
    """
    Creates a City object using `state_id` and HTTP body request fields.
    """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    if fields.get('name') is None:
        return "Missing name", 400
    fields['state_id'] = state_id
    new_city = City(**fields)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """
    Edit a City object using `city_id` and HTTP body request field
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    for key in fields:
        if key in ['id', 'state_id', 'created_at', 'update_at']:
            continue
        if hasattr(city_obj, key):
            setattr(city_obj, key, fields[key])
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200

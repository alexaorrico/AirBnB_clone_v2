#!/usr/bin/python3
"""a new view for City objects that handles all default RESTFul API actions:"""

from flask import abort, jsonify
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """
    Retrieves the list of all City objects of a State.
    If the state_id is not linked to any State object, raise a 404 error
    """
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    cities = [city.to_dict() for city in state_obj.cities]
    return jsonify(cities)


def city(city_id):
    """
    Retrieves a City object based on `city_id`.
    If the city_id is not linked to any City object, raise a 404 error
    """
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


def delete_city(city_id):
    """
    if the city_id is not linked to any City object, raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    city_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_creation(state_id):
    state_obj = storage.get("State", state_id)
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
def add_city(city_id):
    """
    Edit a City object using `city_id` and HTTP body request fields.
    """
    city_obj = storage.get("City", city_id)
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

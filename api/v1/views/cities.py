#!/usr/bin/python3
"""RESTful API action for City object"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.city import City
from models.state import State
<<<<<<< HEAD
from models import storage
=======
from models import storage, storage_t
>>>>>>> e9014739a345ef05ab52e090d5535e1bc9c34875


@app_views.route('/states/<state_id>/cities', methods=["GET"])
def cities_get(state_id):
    """
    get city in state if state_id is specified
    """
    state = storage.get(State, state_id)
    if state:
        if storage_t == 'db':
            cities = [city.to_dict() for city in state.cities]
        else:
            cities = [city.to_dict() for city in state.cities()]
        return jsonify(cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=["GET"])
def city_get(city_id):
    """
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('cities/<city_id>', methods=["DELETE"])
def cities_delete(city_id):
    """
    delete method handler.
    will delete a city with the specified id.
    """
    city = storage.get(City, city_id)

    if city:
        storage.delete(city)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
<<<<<<< HEAD
def city_post():
=======
def city_post(state_id):
>>>>>>> e9014739a345ef05ab52e090d5535e1bc9c34875
    """
    route handler for creating a new city
    """
    if not request.is_json:
        return "Not a JSON", 400
    new_city = request.get_json().get('name')
    if new_city is None:
        return "Missing name", 400
    city = City(name=new_city, state_id=state_id)
    city.save()
    return jsonify(city.to_dict()), 201


<<<<<<< HEAD
@app_views.route('/states/<city_id>', methods=['PUT'])
def city_put(state_id):
=======
@app_views.route('/cities/<city_id>', methods=['PUT'])
def city_put(city_id):
>>>>>>> e9014739a345ef05ab52e090d5535e1bc9c34875
    """
    Returns the City object with the status code 200
    """
    if not request.is_json:
        return "Not a JSON", 400
    data = request.get_json()
    city = storage.get(City, city_id)

    if city is None:
        return abort(404)

    for key, value in data.items():
        if key in ('id', 'state_id', 'created_at', 'updated_at'):
            continue
        else:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200

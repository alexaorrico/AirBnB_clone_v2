#!/usr/bin/python3

"""
a view for City objects that handles all default RESTFul API actions

Author: Khotso Selading and Londeka Dlamini
"""


from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, make_response, request


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def cities_per_state(state_id):
    """retrieves of a list of all city objects for a state"""
    cities_oject = storage.get(State, state_id)

    if not cities_oject:
        abort(404)
    return jsonify([city.to_dict() for city in cities_oject.cities])


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """retrieves a specific city obj"""
    cities_oject = storage.get(City, city_id)

    if not cities_oject:
        abort(404)
    return jsonify(cities_oject.to_dict())


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_city(city_id):
    """deletes specific city object"""
    cities_oject = storage.get(City, city_id)

    if not cities_oject:
        abort(404)

    cities_oject.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def post_city(state_id):
    """adds new city object to filestorage/database"""
    cities_oject = storage.get(State, state_id)
    new_city_object = request.get_json()

    if not cities_oject:
        abort(404)
    if new_city_object is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if new_city_object.get('name') is None:
        return make_response(jsonify({"error": "Missing name"}), 400)

    city = City(**new_city_object)
    city.state_id = cities_oject.id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def put_city(city_id):
    """updates city object on filestorage/database"""
    cities_oject = storage.get(City, city_id)
    new_cities_oject = request.get_json()

    if not cities_oject:
        abort(404)
    if new_cities_oject is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in new_cities_oject.items():
        if key not in {'id', 'created_at', 'updated_at'}:
            setattr(cities_oject, key, value)

    cities_oject.save()
    return make_response(jsonify(cities_oject.to_dict()), 200)

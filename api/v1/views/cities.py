#!/usr/bin/python3
""" Method HTTP for City """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """ Function that retrieves the list of all City """
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)

    all_cities = []
    for city in state.cities:
        all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Function that retrieves a City """
    city = storage.get(City, city_id)
    return abort(404) if city is None else jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Function that deletes a City """
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """ Function that create a City """
    dico = request.get_json()

    state = storage.get(State, state_id)
    if state is None:
        return abort(404)

    if dico is None:
        abort(400, "Not a JSON")

    if dico.get("name") is None:
        abort(400, "Missing name")

    dico['state_id'] = state_id
    new_city = City(**dico)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ Function that update a City """
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)

    dico = request.get_json()

    if dico is None:
        abort(400, "Not a JSON")

    for key, value in dico.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    city.save()

    return jsonify(city.to_dict()), 200

#!/usr/bin/python3
"""
objects that handles all default RestFul API actions:
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


"""Retrieves the list"""
@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """
    Access the api call with on a state object to get its cities
    returns a 404 if not found.
    - POST: Creates a new city object with the state_object linked
    Retrieves the list of all City objects of a State: GET
    """
    state_request = storage.get("State", state_id)
    """If the state_id is not linked to any State object,"""
    if state_request is None:
        abort(404)

    cities = state_request.cities
    city_request = []
    for city in cities:
        city_request.append(city.to_dict())
    return jsonify(city_request)


"""Retrieves a City object"""
@app_views.route('/cities/<city_id>', methods=['GET'])
def get_id(city_id):
    """
    method that retrieves a city filter by id
    """
    city_request = storage.get("City", city_id)
    if city_request is None:
        abort(404)
    return jsonify(city_request.to_dict())


"""Deletes a City"""
@app_views.route('/cities/<city_id>', methods=['DELETE'])
def deleate_id(city_id):
    """
    Deletes a City object: DELETE
    """
    delete_id = storage.get("City", city_id)

    """
    If the city_id is not linked to any City object, raise a 404 error
    """
    if delete_id is None:
        abort(404)

    else:
        delete_id.delete()
        storage.save()
        """return a empty dictionary with status 200"""
        return jsonify({}), 200


"""Creates a City"""
@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_a_city_post(state_id):
    """
    create a city post
    """
    my_state = storage.get("State", state_id)

    """
    If the state_id is not linked to any State object, raise a 404 error
    """
    if my_state is None:
        abort(404)

    """transform the HTTP body request to a dictionary"""
    new_city = request.get_json()

    """If the state_id is not linked to any State object, 404 error"""
    if new_city is None:
        abort(404, "Not a JSON")

    if 'name' not in new_city:
        abort(404, "Missing name")

    new_city = City(name=request.json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


"""Updates a City"""
@app_views.route('/cities/<city_id>', methods=['PUT'])
def Updates_cities(city_id):
    """
    Updates a City object: PUT:
    """
    request_city = request.get_json()
    if request_city is None:
        abort(400, "Not a JSON")

    update_cities = storage.get("City", city_id)
    """If the city_id is not linked to any City object,404 error"""
    if update_cities is None:
        abort(404)

    for key in request_city:
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(update_cities, key, request_city[key])
    storage.save()
    return jsonify(update_cities.to_dict()), 200

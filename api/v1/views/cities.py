#!/usr/bin/python3
"""A scripts that handle RestAPI action for state"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, CNC


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities(state_id):
    """A route that either retrieves all cities of a state
       or Create a city for a state.
       Parameter:
        state_id: string (uuid)
       Return:
        for GET: all cities of a state in json
        for POST: The added new city with 200 status code
    """
    cities = storage.all("City")
    if state is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        state_cities = list(city.to_json() for city in cities.values())
        return jsonify(state_cities)

    if request.method == 'POST':
        request_json = request.get_json()
        if request_json is None:
            abort(400, 'Not a JSON')
        if request_json.get("name") is None:
            abort(400, 'Missing name')
        City = CNC.get("City")
        request_json['state_id'] = state_id
        new_city = City(**request_json)
        new_city.save()
        return jsonify(new_city.to_json()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def city_by_id(city_id):
    """A route handles fetching of cities, deletting cities
    of a state or updating the cities of a state.
    Parameters:
        city_id: string(uuid), Id of the city
    Return:
        for GET: a city of a state is json
        for Delete: empty json
        for Update: updated city
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(city.to_json())

    if request.method == 'DELETE':
        city.delete()
        del city
        return jsonify({})

    if request.method == 'PUT':
        request_obj = request.get_json()
        if request_json is None:
            abort(400, 'Not a JSON')
        city = bm_update(request_json)
        return jsonify(city.to_json()), 200

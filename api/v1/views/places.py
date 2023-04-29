#!/usr/bin/python3
"""A Script that handles RESTFul API Actions on places"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, CNC


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places_of_city(city_id):
    """A route that fetches list of all users or create
    a new place.
    Return:
        for GET: list of places in json format
        for POST: Created place with 200 status code
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        places = storage.all("Place")
        city_place = list(cp.to_json() for cp in places.values()
                          if cp.city_id == city_id)
        return jsonify(city.to_json())

    if request.method == 'POST':
        request_json = request.get_json()
        if request_json is None:
            abort(400, 'Not a JSON')
        user_id = request_json.get("user_id")
        if user_id is None:
            abort(400, 'Missing user_id')
        user = storage.get("User", user_id)
        if user is None:
            abort(404, 'Not found')
        name = request_json.get("name")
        if name is None:
            abort(400, 'Missing name')
        place = CNC.get("Place")
        request_json['city_id'] = city_id
        new_place = place(**request_json)
        new_place.save()
        return jsonify(new_place.to_json()), 201


@app_views('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def places_by_id(place_id):
    """A route that handles GET, DELETE and PUT request
    based on the place_id.
    Parameters:
        user_id: string(uuid), user id
    Return:
        for GET: place object in json
        for DELETE: empty json
        for PUT: updated place with status code
    """
    place = storage.get("Place", place_id)

    if place is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(place.to_json())

    if request.method == 'DELETE':
        place.delete()
        del place
        return jsonify({})

    if request.method == 'PUT':
        request_json = request.get_json()
        if request_json is None:
            abort(400, 'Not a JSON')
        place = bm_update(request_json)
        return jsonify(user.to_json()), 200

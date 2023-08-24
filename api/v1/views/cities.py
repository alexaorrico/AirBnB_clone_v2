#!/usr/bin/python3
"""cities view module"""
from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def cities_from_state_id(state_id):
    """returns all cities of state or 404"""
    state = storage.get(State, state_id)
    if request.method == 'GET':
        if state is None:
            abort(404)
        cities_list = []
        for city, city_details in storage.all(City).items():
            city = city_details.to_dict()
            if city['state_id'] == str(state_id):
                cities_list.append(city)
        if cities_list is not None:
            return jsonify(cities_list)

    if request.method == 'POST':
        # If not valid JSON, error 400
        if state is None:
            abort(404)
        try:
            request_data = request.get_json()
            if 'name' not in request_data:
                abort(400, "Missing name")
            request_data['state_id'] = state_id
            newCity = City(**request_data)
            newCity.save()
        except Exception:
            abort(400, "Not a JSON")
        return jsonify(newCity.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def city_from_id(city_id):
    """returns city from id"""
    # GET, DELETE, PUT both need storage.get(City), so do it once for all
    city = storage.get(City, city_id)
    if request.method == 'GET':
        if city is None:
            abort(404)
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        if city is None:
            abort(404)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if city is None:
            abort(404)
        if request.method == 'PUT':
            try:
                request_data = request.get_json()
                request_data.pop('id', None)
                request_data.pop('state_id', None)
                request_data.pop('created_at', None)
                request_data.pop('updated_at', None)
                for key in request_data.keys():
                    setattr(city, key, request_data[key])
                city.save()
                return jsonify(city.to_dict())

            except Exception:
                return 'Not a JSON\n', 400

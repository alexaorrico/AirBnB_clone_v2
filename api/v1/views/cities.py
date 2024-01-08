#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from flasgger.utils import swag_from


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
@swag_from('swagger_yaml/cities_by_state.yml', methods=['GET', 'POST'])
def cities_per_state(state_id=None):
    """
        cities route to handle http method for requested cities by state
    """
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_cities = storage.all('City')
        state_cities = [obj.to_json() for obj in all_cities.values()
                        if obj.state_id == state_id]
        return jsonify(state_cities)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get("name") is None:
            abort(400, 'Missing name')
        City = CNC.get("City")
        req_json['state_id'] = state_id
        new_object = City(**req_json)
        new_object.save()
        return jsonify(new_object.to_json()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/cities_id.yml', methods=['GET', 'DELETE', 'PUT'])
def cities_with_id(city_id=None):
    """
        cities route to handle http methods for given city
    """
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(city_obj.to_json())

    if request.method == 'DELETE':
        city_obj.delete()
        del city_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        city_obj.bm_update(req_json)
        return jsonify(city_obj.to_json()), 200

#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def states(state_id=None, city_id=None):
    """
    Cities route to handle http method for requested states
    """
    all_cities = storage.all('City')
    fetch_city = "{}.{}".format('City', city_id)
    city_obj = all_cities.get(fetch_city)
    all_states = storage.all('State')
    fetch_state = "{}.{}".format('State', state_id)
    state_obj = all_states.get(fetch_state)

    if request.method == 'GET':
        if city_id and city_obj:
            return jsonify(city_obj.to_json())
        elif state_id and state_obj:
            cities_per_state = [obj.to_json() for obj in all_cities.values()
                                if obj.state_id == state_id == state_id]
            return jsonify(cities_per_state)
        abort(404, 'Not found')

    if request.method == 'DELETE':
        if city_obj:
            city_obj.delete()
            del city_obj
            return jsonify({}), 200
        abort(404, 'Not found')

    if request.method == 'POST':
        if state_id is None or state_obj is None:
            abort(404, 'Not found')
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

    if request.method == 'PUT':
        if city_id and city_obj:
            req_json = request.get_json()
            if city_obj is None:
                abort(404, 'Not found')
            if req_json is None:
                abort(400, 'Not a JSON')
            IGNORE = ['id', 'state_id', 'created_at', 'updated_at']
            attr_dict = {key: val for key, val in req_json.items()
                         if key not in IGNORE}
            city_obj.bm_update(req_json)
            return jsonify(city_obj.to_json()), 200
        abort(404, 'Not found')

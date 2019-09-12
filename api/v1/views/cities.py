#!/usr/bin/python3
'''Creates cities route and returns valid JSON'''
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import request, jsonify, make_response, abort


@app_views.route('states/<state_id>/cities', methods=['GET', 'POST'])
def state_cities_route(state_id):
    '''Returns a JSON of a city object'''
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    if request.method == 'GET':
        city_list = []
        for city in state.cities:
            city_list.append(city.to_dict())
        return jsonify(city_list)

    if request.method == 'POST':
        new_city = request.get_json
        if not new_city:
            abort(400, 'Not a JSON')
        if "name" not in new_city:
            abort(400, 'Missing name')
        new_city['state_id'] = state_id
        print(new_city)
        new_city_obj = City(**new_city)
        new_city_obj.save()
        return jsonify(new_city_obj.to_dict()), 201

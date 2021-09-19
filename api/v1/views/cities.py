#!/usr/bin/python3
""" handles all default RESTFul API actions """
from os import abort, stat
from models.city import City
from flask.json import jsonify
from api.v1.views import app_views
from flask import request, abort

@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['GET', 'POST'])
def all_cities_per_state(state_id=None):
    """ Retrieves the list of all City objects of a State """
    from models import storage
    state = storage.get('State', state_id)
    # no corresponding state is found
    if state is None:
        # Fix this later
        abort(404, 'Not found')
    # State was found and request is GET
    if request.method == "GET":
        all_cities = storage.all('City')
        cities = []
        for city in all_cities.values():
            if city.state_id == state_id:
                cities.append(city.to_json())
        return jsonify(cities)
    if request.method == "POST":
        json_req = request.get_json()
        if json_req is None:
            abort(400, 'Not a Json')
        if json_req.get("name") is None:
            abort(400, 'Missing name')
        json_req["state_id"] = state_id
        new_obj = City(**json_req)
        new_obj.save()
        return jsonify(new_obj.to_json()), 201

@app_views.route('/cities/<city_id>', strict_slashes=False)
def retrieve_city(city_id=None):
    """ retrieve a city by id """
    from models import storage
    city = storage.get('City', city_id)
    # no corresponding city was found
    if city is None:
        return "404 not found"
    if request.method == 'GET':
        return jsonify(city.to_json())
    if request.method == "DELETE":
        city.delete()
        return jsonify({}, 200)
    if request.method == 'PUT':
        json_req = request.get_json()
        if json_req is None:
            abort(400, 'Not a JSON')
        city.update(req_json)
        return jsonify(city.to_json()), 200
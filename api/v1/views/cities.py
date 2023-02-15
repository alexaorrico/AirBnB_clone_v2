#!/usr/bin/python3
"""
handles all RESTFUl API actions for cities
"""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.engine.db_storage import classes


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities_by_state_id(state_id):
    """ defines route for api/v1/states/<state_id>/cities """
    state = storage.get(classes['State'], state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        allCities = [c for c in storage.all('City').values()]
        cities = [c.to_dict() for c in allCities if state_id == c.state_id]
        return jsonify(cities)

    if request.method == 'POST':
        if not request.json:
            return make_response('Not a JSON', 400)
        if 'name' not in request.json:
            return make_response('Missing name', 400)
        cityDict = request.json
        cityDict['state_id'] = state_id
        newObj = classes['City']
        newCity = newObj(**cityDict)
        newCity.save()
        return jsonify(newCity.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def cities_by_city_id(city_id):
    """  defines a route to /cities/<city_id> """
    allCities = [city for city in storage.all('City').values()]
    cities = [city for city in allCities if city.id == city_id]
    if len(cities) == 0:
        abort(404)
    if request.method == 'GET':
        return jsonify(cities[0].to_dict())

    if request.method == 'DELETE':
        storage.delete(cities[0])
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.json:
            return make_response('Not a JSON', 400)
        data = request.json
        for key, value in data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_ap']:
                setattr(cities[0], key, value)
                cities[0].save()
        return jsonify(cities[0].to_dict()), 200

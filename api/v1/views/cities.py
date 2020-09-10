#!/usr/bin/python3
"""city flask triggers"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def citiesretr(state_id):
    """Retrieves the list of all City objects of a State"""
    idstate = storage.get(State, state_id)
    if idstate is None:
        abort(404)
    cities = []
    for city in idstate.cities:
        cities.append(city.to_dict())
    return jsonify(cities)

@app_views.route('/cities/<string:city_id>',
                 methods=['GET'], strict_slashes=False)
def cityid(city_id):
    """Retrieves a City object"""
    cityobj = storage.get(City, city_id)
    if cityobj is None:
        abort(404)
    return jsonify(cityobj.to_dict())

@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete(city_id):
    """deletes a city object"""
    cityobj = storage.get(City, city_id)
    if cityobj is None:
        abort(404)
    storage.delete(cityobj)
    storage.save()
    return (jsonify({}), 200)

@app_views.route('/states/<string:state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def createcity(state_id):
    """Creates a City"""
    citystate = storage.get(State, state_id)
    if citystate is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "missing name"}), 400)
    post_json = request.get_json()
    post_json['state_id'] = state_id
    jsoncity = City(**post_json)
    jsoncity.save()
    return make_response(jsonify(jsoncity.to_dict()), 201)

@app_views.route('/cities/<string:city_id>',
                 methods=['PUT'], strict_slashes=False)
def updatecity(city_id):
    """update a city as json"""
    update = storage.get(City, city_id)
    if update is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(update, key, value)
    update.save()
    return jsonify(update.to_dict())

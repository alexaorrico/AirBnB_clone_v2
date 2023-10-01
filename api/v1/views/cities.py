#!/usr/bin/python3

from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views, City, stoarge


def to_dict():
    """ retrieve an object into a valid JSON"""
    return jsonify({})

@app_views.route('/api/v1/cities', method=['GET'])
def city_list():
    """ retrieve all list of amenities """
    state = stoarge.get("State", state_id)
    if state is None:
        abort(404)
    all_cities = [cities.to_json() for cities in state.cities]
    return jsonify(all_cities)


@app_views.route('/api/v1/cities/<city_id>', method=['GET'])
def city_object(city_id =None):
    """ retrieve all state object """
    city = stoarge.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_json())

@app_views.route('/api/v1/cities/<city_id>', method=['DELETE'])
def city_delete(city_id =None):
    """ delete all state object """
    if city_id is None:
        abort(404)
    city = stoarge.get("City", city_id)
    if city is None:
        abort(404)
    stoarge.delete(city)
    return jsonify({}), 200

@app_views.route('/api/v1/cities', method=['POST'])
def city_create():
    """ create all state object """
    data = None
    try:
        data = request.get_json()
    except:
        data = None
    if data is None:
        return jsonify({"Not a JSON"}), 400
    if 'name' not in data.keys():
        return jsonify({"Missing name"}), 400
    city = City(**data)
    city.save()
    return jsonify(state.to_json()), 201


@app_views.route('/api/v1/cities/<city_id>', method=['PUT'])
def city_update(city_id = None):
    """ update all state object """
    data = None
    try:
        data = request.get_json()
    except:
        data = None
    if data is None:
        return jsonify({"Not a JSON"}), 400
    city = stoarge.get("City", city_id)
    if city is None:
        abort(404)
    for keys, values in data.items():
        if keys not in ('id', 'created_at', 'updated_at'):
            setattr(city, keys, values)
    city.save()
    return jsonify(city.to_json()), 200

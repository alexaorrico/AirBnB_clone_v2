#!/usr/bin/python3
"""
city view
"""

from flask import jsonify, abort, request, make_response, json
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def all_cities():
    """returns a json of all cities"""
    cities = storage.all(City).values()
    jsonlist = []
    for city in cities:
        jsonlist.append(city.to_dict())
    resp = make_response(jsonify(jsonlist))
    resp.status_code = 200
    return resp


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Get a specific city using id"""
    city = storage.get(City, id=city_id)
    if city:
        resp = make_response(jsonify(city.to_dict()))
        resp.status_code = 200
        return resp
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a city Fom DELETE req"""
    city: City = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        resp = make_response(jsonify({'status': 200}))
        resp.status_code = 200
        return resp
    resp = make_response(jsonify)
    resp.status = 404
    return resp


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def create_city():
    """create city"""
    try:
        kwargs = request.get_json(force=True)
    except json.on_json_loading_failed:
        resp = make_response(jsonify({'error': 'Not a JSON'}))
        resp.status_code = 400
        return resp
    if not isinstance(kwargs, dict) or 'name' not in kwargs:
        resp = make_response(jsonify({'error': 'Missing Name'}))
        resp.status_code = 400
        return resp
    city = City(**kwargs)
    storage.new(city)
    storage.save()
    resp = make_response(jsonify(city.to_dict()))
    resp.status_code = 201

    return resp


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updated_city(city_id):
    """update city"""
    city: City = storage.get(city_id)
    if not city:
        abort(404)

    try:
        kwargs: dict = request.get_json(force=True)
        for key in kwargs.keys():
            if key in ('id', 'created_at', 'updated_at'):
                kwargs.pop(key)
    except json.on_json_loading_failed:
        resp = make_response(jsonify({'error': 'Not a JSON'}))
        resp.status_code = 400
        return resp
    if not isinstance(kwargs, dict):
        resp = make_response(jsonify({'error': 'Missing Name'}))
        resp.status_code = 400
        return resp
    city_dict = city.to_dict()
    city_dict.update(kwargs)
    city = City(**city_dict)
    storage.new(city)
    storage.save()
    resp = make_response(jsonify(city.to_dict()))
    resp.status_code = 201

    return resp

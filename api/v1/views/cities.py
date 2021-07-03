#!/usr/bin/python3
""" prepares data for easier viewing """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import OperationalError


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def get_all_create_cities(state_id):
    """ Returns all the cities in a state obj in json  or makes a new one"""
    if state_id:
        state = storage.get('State', state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    if request.mimetype != 'application/json':
        return jsonify(error="Not a JSON"), 400
    try:
        city_json = request.get_json()
    except BadRequest:
        return jsonify(error="Not a JSON"), 400
    city = City(**city_json)
    setattr(city, 'state_id', state.id)
    try:
        city.save()
    except OperationalError:
        return jsonify(error="Missing name"), 400
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def get_put_del_city(city_id):
    """ Returns all the state obj in json """
    if city_id:
        city = storage.get('City', city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({})
    """at this point we putting, check the payload"""
    if request.mimetype != 'application/json':
        return jsonify(error="Not a JSON"), 400
    try:
        city_json = request.get_json()
    except BadRequest:
        return jsonify(error="Not a JSON"), 400

    if city_json.get('id'):
        city_json.pop('id')
    if city_json.get('created_at'):
        city_json.pop('created_at')
    if city_json.get('updated_at'):
        city_json.pop('updated_at')
    for k, v in city_json.items():
        setattr(city, k, v)
        city.save()
    return jsonify(city.to_dict())

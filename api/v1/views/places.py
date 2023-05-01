#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger.utils import swag_from
from models import storage, CNC
from os import environ


STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@swag_from('swagger_yaml/places_by_city.yml', methods=['GET', 'POST'])
@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places_per_city(city_id=None):
    """
        places route to handle http method for requested places by city
    """
    city_obj = storage.get('City', city_id)
    if not city_obj:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_places = storage.all('Place')
        city_places = [
            obj.to_json() for obj in all_places.values()
            if obj.city_id == city_id
        ]
        return jsonify(city_places)

    if request.method == 'POST':
        req_json = request.get_json()
        if not req_json:
            abort(400, 'Not a JSON')
        user_id = req_json.get("user_id")
        if not user_id:
            abort(400, 'Missing user_id')
        user_obj = storage.get('User', user_id)
        if not user_obj:
            abort(404, 'Not found')
        if not req_json.get("name"):
            abort(400, 'Missing name')
        Place = CNC.get("Place")
        req_json['city_id'] = city_id
        new_object = Place(**req_json)
        new_object.save()
        return jsonify(new_object.to_json()), 201


@swag_from('swagger_yaml/places_id.yml', methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def places_with_id(place_id=None):
    """
        places route to handle http methods for given place
    """
    place_obj = storage.get('Place', place_id)
    if not place_obj:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(place_obj.to_json())

    if request.method == 'DELETE':
        place_obj.delete()

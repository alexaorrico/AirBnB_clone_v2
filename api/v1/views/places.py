#!/usr/bin/python3
"""
Views for Places
"""
from flask import request, abort, jsonify
from models import storage
from models.place import Place
from api.v1.views import app_views


@app_views.route('cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places(city_id=None):
    """
    Retrieves the list of all Place objects: GET /api/v1/places
    Creates a Place: POST /api/v1/places
    """
    if request.method == 'GET':
        list_places = []
        city = storage.get('City', city_id)
        if city:
            for place in city.places:
                list_places.append(place.to_dict())
            return jsonify(list_places), 200
        abort(404)

    if request.method == 'POST':
        request_json = request.get_json()
        if not request_json:
            return jsonify(error='Not a JSON'), 400
        if 'name' not in request_json:
            return jsonify(error='Missing name'), 400
        if 'user_id' not in request_json:
            return jsonify(error='Missing user_id'), 400
        city = storage.get('City', city_id)
        if city:
            request_json['place_id'] = place.id
            place = Place(**request_json)
            storage.new(place)
            storage.save()
            return jsonify(place.to_dict()), 201
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def place(place_id=None):
    """
    Retrieves the list of all Place objects: GET /api/v1/places
    Creates a Place: POST /api/v1/places
    """
    if request.method == 'GET':
        place = storage.get('Place', place_id)
        if place:
            return jsonify(place.to_dict()), 200
        abort(404)

    if request.method == 'DELETE':
        place = storage.get('Place', place_id)
        if place:
            storage.delete(place)
            storage.save()
            return jsonify({}), 200
        abort(404)

    if request.method == 'PUT':
        request_json = request.get_json()
        if not request_json:
            return jsonify(error='Not a JSON'), 400
        place = storage.get('Place', place_id)
        if place:
            for key, value in request_json.items():
                if key not in ["__class__", "id", "user_id",
                               "city_id", "created_at", "updated_at"]:
                    setattr(place, key, value)
            storage.save()
            return jsonify(place.to_dict()), 200
        abort(404)

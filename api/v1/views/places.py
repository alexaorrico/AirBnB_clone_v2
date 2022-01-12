#!/usr/bin/python3
"""creates a new view for places"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def allPlaces(city_id):
    """retrieves a list of all place objects"""
    if request.method == "GET":
        allPlaces = []
        city_data = storage.get(City, city_id)

        if city_data is not None:
            for key in city_data.places:
                allPlaces.append(key.to_dict())
            return jsonify(allPlaces)
        abort(404)

    if request.method == "POST":
        if storage.get(City, city_id) is None:
            abort(404)

        if not request.is_json:
            abort(400, description='Not a JSON')

        jsonReq = request.get_json()
        jsonReq['city_id'] = city_id

        if 'user_id' not in jsonReq:
            abort(400, description='Missing user_id')

        if storage.get(User, jsonReq['user_id']) is None:
            abort(404)

        if 'name' not in jsonReq:
            abort(400, description='Missing name')

        newPlace = Place(**jsonReq)

        storage.new(newPlace)
        storage.save()

        return jsonify(newPlace.to_dict()), 201


@app_views.route('/places/<places_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def places_ident(places_id):
    """updates a place object"""
    if request.method == "GET":
        place_info = storage.get(Place, places_id)
        if place_info is not None:
            return jsonify(place_info.to_dict())
        abort(404)

    if request.method == "PUT":
        ignoreKeys = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
        place_info = storage.get(Place, places_id)

        if place_info is None:
            abort(404)

        if not request.is_json:
            return "Not a JSON", 400

        for key, value in request.get_json().items():
            if key not in ignoreKeys:
                setattr(place_info, key, value)
        storage.save()
        return jsonify(place_info.to_dict()), 200

    if request.method == "DELETE":
        place_info = storage.get(Place, places_id)
        if place_info:
            storage.delete(place_info)
            storage.save()
            return jsonify({}), 200
        abort(404)

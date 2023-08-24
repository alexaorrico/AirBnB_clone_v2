#!/usr/bin/python3#!/usr/bin/python3
"""places view module"""
from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_from_city_id(city_id):
    """returns all places of city or 404"""
    city = storage.get(City, city_id)
    if request.method == 'GET':
        if city is None:
            abort(404)
        places_list = []
        for place, place_details in storage.all(Place).items():
            place = place_details.to_dict()
            if place['city_id'] == str(city_id):
                places_list.append(place)
        if places_list is not None:
            return jsonify(places_list)

    if request.method == 'POST':
        # If not valid JSON, error 400
        if city is None:
            abort(404)
        request_data = request.get_json()
        if request_data is None:
            abort(400, "Not a JSON")
        if 'name' not in request_data:
            abort(400, "Missing name")
        if 'user_id' not in request_data:
            abort(400, "Missing user_id")
        request_data['city_id'] = city_id
        user = storage.get(User, request_data.get('user_id'))
        if user is None:
            abort(404)
        newPlace = Place(**request_data)
        newPlace.save()
        return jsonify(newPlace.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def place_from_id(place_id):
    """returns place from id"""
    # GET, DELETE, PUT both need storage.get(Place), so do it once for all
    place = storage.get(Place, place_id)
    if request.method == 'GET':
        if place is None:
            abort(404)
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        if place is None:
            abort(404)
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if place is None:
            abort(404)
        try:
            request_data = request.get_json()
            request_data.pop('id', None)
            request_data.pop('city_id', None)
            request_data.pop('created_at', None)
            request_data.pop('updated_at', None)
            request_data.pop('user_id', None)
            for key in request_data.keys():
                setattr(place, key, request_data[key])
            place.save()
            return jsonify(place.to_dict()), 200

        except Exception:
            return 'Not a JSON\n', 400

#!/usr/bin/python3
""" New view for places object that handles all
default RESTFul API actions. """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_place_id(place_id):
    """ Retrieves, updates or deletes a place object given its id. """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        req_data = request.get_json()
        if not req_data:
            abort(400, description='Not a JSON')

        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

        for key, value in req_data.items():
            if key not in ignore_keys:
                setattr(place, key, value)

        storage.save()
        return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def city_places(city_id):
    """ Retrieves all Place objects of a city and creates
    a new place object in a city given the city's id.
    Returns 404 error if id is not found.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        list_places = [place.to_dict() for place in city.places]

        return jsonify(list_places)

    if request.method == 'POST':
        req_data = request.get_json()
        if not req_data:
            abort(400, description='Not a JSON')

        if "user_id" not in req_data:
            abort(400, description="Missing user_id")

        user = storage.get(User, req_data['user_id'])
        if not user:
            abort(404)

        if "name" not in req_data:
            abort(400, description="Missing name")

        req_data['city_id'] = city_id
        place = Place(**req_data)
        place.save()
        return make_response(jsonify(place.to_dict()), 201)

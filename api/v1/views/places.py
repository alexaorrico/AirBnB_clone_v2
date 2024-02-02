#!/usr/bin/python3
"""
A view for Place objects that handles all default RESTFul API Actions
"""


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['GET', 'POST'])
def places_of_city(city_id):
    """ Function for retrieving and posting places by city_id """
    city = storage.all(City, city_id)
    # Checking if the city exists
    if city is None:
        abort(404)
    places_obj = city.places
    # Action for GET method
    if request.method == 'GET':
        places = []
        for obj in places_obj:
            places.append(obj.to_dict())
        return jsonify(places)
    # Action for POST method
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if storage.get(User, user_id) is None:
        abort(404)
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    data['city_id'] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def place_by_id(place_id):
    """ Function that retrieves, delete or update a place by id """
    place = storage.get(Place, place_id)
    # Check if the place exists
    if place is None:
        abort(404)
    # Action for GET method
    if request.method == 'GET':
        return jsonify(place.to_dict())
    # Action for DELETE method
    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    # Action for PUT method
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key in data.keys():
        if key not in ignore_keys:
            setattr(place, key, data[key])
    storage.save()
    return jsonify(place.to_dict()), 200

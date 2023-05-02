#!/usr/bin/python3
"""
creating a new view for place objects that handles all default RESTful api
"""
from flask import request, abort, jsonify, make_response
from models.city import City
from models.place import Place
from models.place import Place
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', method=['GET'],
                 strict_slashes=False)
def places_in_city(city_id):
    """
    getting a list of all the places in a city
    """
    p_list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    for place in city.places:
        p_list.append(place.to_dict())

    return jsonify(p_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_a_place(place_id):
    """
    gets a place out of the list of poaces
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place = place.to_dict()
    return jsonify(place)


@app_views.route('/places/place_id', methods=['DELETE'], strict_slashes=False)
def delete_place_obj(place_id):
    """
    deletes an instance of a place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place_obj(city_id):
    """
    creates a new instance of the place object
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    if "user_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    place_info = request.get_json()
    user_id = place_info['user_id']

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    place_info['city_id'] = city.id
    place_info['user_id'] = user.id

    newPlace = Place(**place_info)
    storage.new()
    storage.save(newPlace)
    return jsonify(newPlace.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    updates a place instance with new values
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    update_info = request.get_json()
    for key, value in update_info.items():
        if key not in ['id', 'created_at', 'updated_at']:
            place_updated = setattr(place, key, value)

    storage.save()
    return jsonify(place_updated.to_dict()), 200

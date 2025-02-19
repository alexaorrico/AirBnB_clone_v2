#!/usr/bin/python3
"""Handles all default RESTful API actions for Place objects"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import abort, jsonify, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False, endpoint='get_all_places')
def get_all_places_in_city(city_id):
    """Returns a JSON list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    list_of_places = [place.to_dict() for place in city.places]

    return jsonify(list_of_places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False, endpoint='get_place')
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False, endpoint='delete_place')
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False, endpoint='create_place')
def create_place(city_id):
    """Creates a Place"""
    if storage.get(City, city_id) is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    json_data = request.get_json()
    user_id = json_data.get('user_id')
    if user_id is None:
        abort(400, description='Missing user_id')

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    user_data = request.get_json()
    if 'name' not in user_data:
        abort(400, description='Missing name')

    json_data['city_id'] = city_id  # adds the city_id attribute
    json_data['user_id'] = user_id  # adds the user_id attribute

    # sends complete json_data to be used to create the Place object
    new_place = Place(**json_data)

    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False, endpoint='update_place')
def update_place(place_id):
    """Updates a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    json_data = request.get_json()

    for key, value in json_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict()), 200

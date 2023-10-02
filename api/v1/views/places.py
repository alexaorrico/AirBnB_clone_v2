#!/usr/bin/python3
"""
This module defines the view for Place objects.
"""


from flask import Flask, jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
app = Flask(__name__)


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<string:place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object by its id."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by its id."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<string:city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a new Place object in a City."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400

    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_place = Place(city_id=city_id, user_id=user_id, **data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object by its id."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Searches for Place objects based on the provided JSON criteria."""
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places = []

    if not states and not cities:
        places = storage.all(Place).values()
    else:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                cities += [city.id for city in state.cities]

        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places += city.places

    if amenities:
        places = [place for place in places if all
                  (amenity_id in place.amenity_ids
                   for amenity_id in amenities)]

    result = [place.to_dict() for place in places]
    return jsonify(result)

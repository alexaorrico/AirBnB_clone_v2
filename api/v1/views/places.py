#!/usr/bin/python3
"""Flask Places"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """Retrieves the list of all Place objects of a City"""

    id = storage.get("City", city_id)
    if id is None:
        abort(404)
    dic_p = []
    for id in id.places:
        dic_p.append(id.to_dict())
    return jsonify(dic_p)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_places(place_id):
    """Deletes a Place object"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""

    if not storage.get("City", city_id):
        abort(404)

    input_json = request.get_json()
    if not input_json:
        abort(400, 'Not a JSON')

    if "user_id" not in input_json:
        abort(400, 'Missing user_id')

    if storage.get("User", input_json["user_id"]) is None:
        abort(404)

    if "name" not in input_json:
        abort(400, 'Missing name')

    new = Place(user_id=input_json["user_id"],
                name=input_json["name"],
                city_id=city_id)

    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_a_places(place_id):
    """Updates a Place object"""

    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    input_json = request.get_json()

    if input_json is None:
        abort(400, "Not a JSON")

    for key, value in input_json.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    retrieves all Place objects depending of the JSON in the body
    of the request
    """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')

    all_empty = False
    states_ids = []
    cities_ids = []
    amenities_ids = []

    if data:
        for key in data:
            if key == "states":
                states_ids = data.get("states", [])
            elif key == "cities":
                cities_ids = data.get("cities", [])
            elif key == "amenities":
                amenities_ids = data.get("amenities", [])
    else:
        all_empty = True

    results = []
    all_cities = []
    if all_empty or (not states_ids and not cities_ids):
        results = list(storage.all(Place).values())
    if states_ids:
        for state_id in states_ids:
            state = storage.get(State, str(state_id))
            state_cities = state.cities
            for city in state_cities:
                all_cities.append(str(city.id))
                places = city.places
                results.extend(places)
    if cities_ids:
        for city_id in cities_ids:
            if str(city_id) in all_cities:
                continue
            city = storage.get(City, str(city_id))
            places = city.places
            results.extend(places)

    return_results = []
    if amenities_ids:
        for place in results:
            qualified = True
            amenities = place.amenities
            if not amenities or amenities == []:
                qualified = False
            place_amenities_ids = [str(amenity.id) for amenity in amenities]
            for id_ in amenities_ids:
                if id_ not in place_amenities_ids:
                    qualified = False
                    break
            if qualified:
                return_results.append(place.to_dict())
    else:
        return_results = [result.to_dict() for result in results]
    return jsonify(return_results)

#!/usr/bin/python3
"""
places view routes
"""
from functools import reduce
from operator import concat

from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage, storage_t
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route(
    "/cities/<city_id>/places",
    methods=["GET", "POST"],
    strict_slashes=False,
)
def city_places(city_id):
    """Handles /cities/<city_id>/places endpoint

    Returns:
        json: list of all places or the newly added place
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == "POST":
        place_data = request.get_json(silent=True)
        if place_data is None:
            return jsonify(error="Not a JSON"), 400

        if "user_id" not in place_data:
            return jsonify(error="Missing user_id"), 400
        elif "name" not in place_data:
            return jsonify(error="Missing name"), 400
        else:
            user = storage.get(User, place_data["user_id"])
            print(user)
            if user is None:
                abort(404)
            place_data["city_id"] = city.id
            place = Place(**place_data)
            storage.new(place)
            storage.save()
            return jsonify(place.to_dict()), 201
    else:
        return jsonify([place.to_dict() for place in city.places])


@app_views.route(
    "/places/<place_id>",
    methods=["GET", "DELETE", "PUT"],
    strict_slashes=False,
)
def places(place_id):
    """Handles /places/<place_id> endpoint

    Returns:
        json: place or empty
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return jsonify({})
    elif request.method == "PUT":
        place_data = request.get_json(silent=True)
        if place_data is None:
            return jsonify(error="Not a JSON"), 400

        for key, value in place_data.items():
            if key not in [
                    "id", "user_id", "city_id", "created_at", "updated_at"
            ]:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict())

    else:
        return jsonify(place.to_dict())


@app_views.route(
    "/places_search",
    methods=["POST"],
    strict_slashes=False,
)
def search_places():
    """searches places by the given states, cities and amenities
    """
    query = request.get_json(silent=True)
    if query is None:
        return jsonify(error="Not a JSON"), 400

    state_ids = query.get("states", [])
    city_ids = query.get("cities", [])
    amenity_ids = query.get("amenities", [])

    search_result = [place.to_dict() for place in storage.all(Place).values()]
    if len(query) == 0 or len(state_ids + city_ids + amenity_ids) == 0:
        return jsonify(search_result)

    search_result = filter_places_by_cities(search_result, city_ids, state_ids)
    search_result = filter_places_by_amenities(search_result, amenity_ids)

    return jsonify(search_result)


def filter_places_by_cities(places, city_ids, state_ids=[]):
    if len(state_ids + city_ids) > 0:
        state_cities = reduce(
            concat,
            [
                state.cities for state in storage.all(State).values()
                if state.id in set(state_ids)
            ],
            [],
        )
        city_ids.extend([city.id for city in state_cities])

        return [
            place for place in places
            if place.get("city_id", None) in set(city_ids)
        ]

    return places


def filter_places_by_amenities(places, amenity_ids):
    if len(amenity_ids) > 0:
        amenity_ids = set(amenity_ids)
        fileted_place_ids = []
        for place in places:
            if storage_t == 'db':
                place_amenity_ids = {amenity.id for amenity in place.amenities}
            else:
                place_amenity_ids = place.amenity_ids

            if len(amenity_ids.intersection(place_amenity_ids)) != 0:
                fileted_place_ids.append(place.id)
        return [place for place in places if place["id"] in fileted_place_ids]

    return places

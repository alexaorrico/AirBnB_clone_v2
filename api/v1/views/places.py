#!/usr/bin/python3
"""
places view routes
"""
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

    search_result = []
    if len(query) == 0 or len(state_ids + city_ids) == 0:
        search_result = [place for place in storage.all(Place).values()]
    elif len(city_ids + state_ids) > 0:
        cities = get_cities(city_ids, state_ids)
        for city in cities:
            search_result.extend(city.places)

    search_result = filter_places_by_amenities(search_result, amenity_ids)
    search_result = [place.to_dict() for place in search_result]
    for place in search_result:
        place.pop("amenities", None)
        place.pop("amenity_ids", None)

    return jsonify(search_result)


def get_cities(city_ids=[], state_ids=[]):
    cities = []
    cities.extend(
        list(
            filter(lambda x: x is not None,
                   [storage.get(City, id) for id in city_ids])))

    states = list(
        filter(lambda x: x is not None,
               [storage.get(State, id) for id in state_ids]))
    for state in states:
        cities.extend(state.cities)
    return list(set(cities))


def filter_places_by_amenities(places, amenity_ids):
    if len(amenity_ids) > 0:
        amenity_ids = set(amenity_ids)
        fileted_place_ids = []
        for place in places:
            if storage_t == 'db':
                place_amenity_ids = {amenity.id for amenity in place.amenities}
            else:
                place_amenity_ids = set(place.amenity_ids)

            if all(id in place_amenity_ids for id in amenity_ids):
                fileted_place_ids.append(place.id)
        return [place for place in places if place.id in fileted_place_ids]
    return places

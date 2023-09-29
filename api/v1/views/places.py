#!/usr/bin/python3
"""Handles all RESTful API actions for `Place`"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State


@app_views.route("/cities/<city_id>/places")
def places(city_id):
    """Get all places in a city

    Args:
        city_id (str): ID of the City

    Returns:
        list: All the places in that city

    Raises:
        404: If the specified city_id does not exist
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    result = []

    for place in city.places:
        result.append(place.to_dict())

    return jsonify(result)


@app_views.route("/places/<place_id>")
def place(place_id):
    """Get a place

    Args:
        place_id (str): ID of the place

    Returns:
        dict: Place JSON

    Raises:
        404: If the specified place_id does not exist
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Delete a place

    Args:
        place_id (str): ID of the place

    Returns:
        dict: An empty JSON

    Raises:
        404: If the specified place_id does not exist
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    place.delete()
    storage.save()

    return jsonify(place.to_dict())


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """Create a places in a city.

    Args:
        city_id (str): ID of the City where the place will be created.

    Returns:
        dict: The created place.

    Raises:
        404: If the specified city_id does not exist.
        400: If the request body is not a valid JSON or if it is missing the
             user_id or name.
    """
    payload = request.get_json()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not payload:
        abort(400, "Not a JSON")
    if "user_id" not in payload:
        abort(400, "Missing user_id")
    if not storage.get(User, payload["user_id"]):
        abort(404)
    if "name" not in payload:
        abort(400, "Missing name")

    place = Place(city_id=city_id, **payload)
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """Update a place.

    Args:
        place_id (str): ID of the place to update.

    Returns:
        dict: Updated place in JSON.

    Raises:
        404: If the specified place_id does not exist.
        400: If the request body is not a valid JSON.
    """
    place = storage.get(Place, place_id)
    payload = request.get_json()
    if not place:
        abort(404)
    if not payload:
        abort(400, "Not a JSON")

    for key, value in place.to_dict().items():
        if key not in [
            "id",
            "user_id",
            "city_id",
            "created_at",
            "updated_at",
            "__class__",
        ]:
            setattr(place, key, payload[key] if key in payload else value)
    place.save()

    return jsonify(place.to_dict())


@app_views.route("/places_search", methods=["POST"])
def search():
    # If the HTTP request body is not valid JSON
    guide = request.get_json()
    if not guide:
        abort(400, "Not a JSON")

    state_ids = guide.get("states")
    city_ids = guide.get("cities")
    amenity_ids = guide.get("amenities")
    result = []

    # If the JSON body is empty or each list of all keys are empty:
    # retrieve all Place objects
    if not guide and not state_ids and not city_ids:
        result = storage.all(Place)

    # If states list is not empty, results should
    # include all Place objects for each State id listed
    if state_ids:
        for state_id in state_ids:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        result.append(place)

    # If cities list is not empty, results should
    # include all Place objects for each City id listed
    if city_ids:
        for city_id in city_ids:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    if place not in result:
                        result.append(place)

    # If amenities list is not empty, limit search results to
    # only Place objects having all Amenity ids listed
    if amenity_ids:
        for place in result:
            if place.amenities:
                place_amenity_ids = [amenity.id for amenity in place.amenities]
                for amenity_id in amenity_ids:
                    if amenity_id not in place_amenity_ids:
                        result.remove(place)
                        break

    # serialize to json
    result = [storage.get(Place, place.id).to_dict() for place in result]
    # remove relationship keys with list comprehension and
    # dictionary comprehension
    keys_to_remove = ["amenities", "reviews", "amenity_ids"]
    result = [
        {k: v for k, v in place_dict.items() if k not in keys_to_remove}
        for place_dict in result
    ]

    return jsonify(result)

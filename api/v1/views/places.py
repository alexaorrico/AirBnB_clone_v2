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
    """Get all places in a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    result = [place.to_dict() for place in city.places]
    return jsonify(result)


@app_views.route("/places/<place_id>")
def place(place_id):
    """Get a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Delete a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    place.delete()
    storage.save()

    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """Create a place in a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    payload = request.get_json()
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
    """Update a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")

    for key, value in place.to_dict().items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at", "__class__"]:
            setattr(place, key, payload.get(key, value))
    place.save()

    return jsonify(place.to_dict())


@app_views.route("/places_search", methods=["POST"])
def search():
    """Search for places"""
    guide = request.get_json()
    if not guide:
        abort(400, "Not a JSON")

    state_ids = guide.get("states", [])
    city_ids = guide.get("cities", [])
    amenity_ids = guide.get("amenities", [])

    result = []
    for state_id in state_ids:
        state = storage.get(State, state_id)
        if state:
            result.extend(state.cities)

    for city_id in city_ids:
        city = storage.get(City, city_id)
        if city:
            result.append(city)

    for amenity_id in amenity_ids:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            result.extend(amenity.places)

    result = [storage.get(Place, item.id).to_dict() for item in set(result)]
    return jsonify(result)

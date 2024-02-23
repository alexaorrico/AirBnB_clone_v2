#!/usr/bin/python3
"""This is the places api module"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Place, City, User, State, City, Amenity
"""These are the imported modules and or packages"""


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves a list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city:
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    else:
        abort(404)


@app_views.route("/places/<place_id>",
                 methods=["GET"],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """Retrieves a Place object by ID"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """Deletes a Place object by ID"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    if "name" not in data:
        abort(400, description="Missing name")
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    place = Place(**data)
    place.city_id = city_id
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def update_place_by_id(place_id):
    """Updates a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def search_places():
    """Retrieves Place objects based on search criteria in the request body"""
    try:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")

        states = data.get("states", [])
        cities = data.get("cities", [])
        amenities = data.get("amenities", [])

        places = storage.all(Place).values()

        if states:
            places = [place for place in places
                      if place.city.state_id in states]

        if cities:
            places += [place for place in storage.get(City, city_id).places
                       for city_id in cities]

        if amenities:
            places = [place for place in places
                      if all(amenity.id in place.amenities
                             for amenity_id in amenities)]

        return jsonify([place.to_dict() for place in places])

    except Exception as e:
        abort(400, description=str(e))

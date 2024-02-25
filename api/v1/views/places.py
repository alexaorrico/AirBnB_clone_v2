#!/usr/bin/python3
"""Places hanlders."""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State


@app_views.route(
    "/cities/<string:city_id>/places", methods=["GET"], strict_slashes=False
)
def get_places(city_id):
    """Retrieve all the places of the specified city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route(
    "/places/<string:place_id>",
    methods=["GET"],
    strict_slashes=False,
)
def get_place(place_id):
    """Get info about specified place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    "/places/<string:place_id>", methods=["DELETE"], strict_slashes=False
)
def delete_place(place_id):
    """Delete specified place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route(
    "/cities/<string:city_id>/places", methods=["POST"], strict_slashes=False
)
def create_place(city_id):
    """Create a new city."""
    req = request.get_json(silent=True)
    if not req:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if "user_id" not in req:
        abort(400, "Missing user_id")
    user = storage.get(User, req["user_id"])
    if user is None:
        abort(404)
    if "name" not in req:
        abort(400, "Missing name")
    req["city_id"] = city_id
    place = Place(**req)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route(
    "/places/<string:place_id>", methods=["PUT"], strict_slashes=False
)
def update_place(place_id):
    """Update specified place."""
    req = request.get_json(silent=True)
    if not req:
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for attr, val in request.get_json().items():
        if attr not in [
            "id",
            "created_at",
            "updated_at",
            "city_id",
            "user_id",
        ]:
            setattr(place, attr, val)
    place.save()
    return jsonify(place.to_dict())


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def post_places_search():
    """Search for a specific place."""
    req = request.get_json(silent=True)
    if req is None:
        abort(400, "Not a JSON")
    states = req.get("states", [])
    cities = req.get("cities", [])
    amenities = req.get("amenities", [])
    if states == cities == amenities == [] or not req or not len(req):
        places = storage.all(Place).values()
        places = []
        for place in places:
            places.append(place.to_dict())
        return jsonify(places)
    places = []
    if states:
        states_obj = [storage.get(State, state_id) for state_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            places.append(place)
    if cities:
        cities_obj = [storage.get(City, city_id) for city_id in cities]
        for city in state.cities:
            if city:
                for place in city.places:
                    if place not in places:
                        places.append(place)
    if amenities:
        if not places:
            places = storage.all(Place).values()
        amenities_obj = [
            storage.get(Amenity, amenity_id) for amenity_id in amenities
        ]
        places = [
            place
            for place in places
            if all(amenity in place.amenities for amenity in amenities_obj)
        ]
    confirmed_places = []
    for place in places:
        d = place.to_dict()
        d.pop("amenities", None)
        confirmed_places.append(d)
    return jsonify(confirmed_places)

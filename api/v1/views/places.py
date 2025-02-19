#!/usr/bin/python3
"""Place objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from flask import abort, request, jsonify


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["GET"])
def places(city_id):
    """show places"""
    places_list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["GET"])
def get_place(place_id):
    """Retrieves a City object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["DELETE"])
def place_delete(place_id):
    """delete method"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["POST"])
def create_place(city_id):
    """create a new post req"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    if "name" not in data:
        abort(400, "Missing name")
    new_place = Place(city_id=city.id, **data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["PUT"])
def update_placey(place_id):
    """update place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    place.name = data.get("name", place.name)
    place.description = data.get("description",
                                 place.description)
    place.number_rooms = data.get("number_rooms",
                                  place.number_rooms)
    place.number_bathrooms = data.get("number_bathrooms",
                                      place.number_bathrooms)
    place.max_guest = data.get("max_guest", place.max_guest)
    place.price_by_night = data.get("price_by_night", place.price_by_night)
    place.latitude = data.get("latitude", place.latitude)
    place.longitude = data.get("longitude", place.longitude)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", strict_slashes=False,
                 methods=["POST"])
def search_places():
    """
        Retrieves all Place objects
        depending of the JSON in the body of the request.
    """
    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)

#!/usr/bin/python3
"""
This module contains a view for Places object that handles all default
RESTful API actions(basically CRUD operations)
"""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route(
    "/cities/<city_id>/places", methods=["GET"], strict_slashes=False
)
def places(city_id):
    """ This method gets all instances of place """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.place]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place_by_id(place_id):
    """ This function gets a place by id """
    places = storage.get(Place, place_id)
    if not places:
        abort(404, "Not found")
    return jsonify(places.to_dict())


@app_views.route(
    "/places/<place_id>", methods=["DELETE"], strict_slashes=False
)
def delete_place_by_id(place_id):
    """ This function deletes a place by id """
    places = storage.get("Place", place_id)
    if not places:
        abort(404, "Not found")
    storage.delete(places)
    storage.save()
    return jsonify(places.to_dict()), 200


@app_views.route(
    "/cities/<city_id>/places", methods=["POST"], strict_slashes=False
)
def create_place(city_id):
    """ This function creates a new place """
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")

    if "user_id" not in new_place:
        abort(400, "Missing user_id")

    user = storage.get(User, new_place['user_id'])

    if not user:
        abort(404)

    if "name" not in new_place:
        abort(400, "Missing name")

    new_place['city_id'] = city_id
    places = Place(**new_place)
    storage.save()
    return make_response(jsonify(places.to_dict(), 201))


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place_by_id(place_id):
    """ This function updates a place by its id """
    places = storage.get("Place", place_id)

    if not places:
        abort(404, "Not found")

    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")

    ignore_list = ["id", "user_id", "city_id", "created_at", "updated_at"]

    for key, value in new_place.items():
        if key not in ignore_list:
            setattr(places, key, value)
    storage.save()
    return make_response(jsonify(places.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    places = request.get_json()

    if places and len(places):
        states = places.get('states', None)
        cities = places.get('cities', None)
        amenities = places.get('amenities', None)

    if not places or not len(places) or (
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
        states_obj = [storage.get("State", s_id) for s_id in states]
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
        amenities_obj = [storage.get("Amenity", a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)

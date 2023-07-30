#!/usr/bin/python3
"""
This module handles the view for Place objects that handles
all default RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import place_views, city_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@city_views.route("/<string:city_id>/places", methods=["GET"])
def list_places(city_id):
    """Retrieves the list of all places objects in a city"""
    places_objs = storage.all(Place)
    places_list = []
    for place in places_objs.values():
        if place.city_id == city_id:
            places_list.append(place.to_dict())

    if not places_list:
        abort(404)
    return jsonify(places_list)


@place_views.route("/<string:place_id>", methods=["GET"])
def get_place(place_id):
    """Retrieves an Place object by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@place_views.route("/<string:place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Deletes a Place object by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@city_views.route("/<string:city_id>/places", methods=["POST"])
def create_place(city_id):
    """Creates a new Place and stores it"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_data = request.get_json()
    if not place_data:
        abort(400, "Not a JSON")
    if 'user_id' not in place_data:
        abort(400, "Missing user_id")
    else:
        user = storage.get(User, place_data['user_id'])
        if user is None:
            abort(404)
    if 'name' not in place_data:
        abort(400, "Missing name")
    place = Place(**place_data)
    setattr(place, "city_id", city_id)
    place.save()
    return jsonify(place.to_dict()), 201


@place_views.route("/<string:place_id>", methods=["PUT"])
def update_place(place_id):
    """Updates a Place given by place_id and stores it"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    if len(request.data) == 0:
        abort(400, "Not a JSON")
    place_data = request.get_json()
    if not place_data:
        abort(400, "Not a JSON")
    for key, value in place_data.items():
        keys_to_ignore = ["id", "user_id", "city_id",
                          "created_at", "updated_at"]
        if key not in keys_to_ignore:
            setattr(place, key, value)
    place.save()
    storage.save()
    place = place.to_dict()
    return jsonify(place), 200

#!/usr/bin/python3
"""
File that configures the routes of place
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from sqlalchemy.exc import IntegrityError


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_places(city_id=None):
    """
    Function that returns all the places of a city
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = city.places
    places_list = []
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", strict_slashes=False)
def get_place(place_id=None):
    """
    Function that returns a place
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["DELETE"])
def delete_place(place_id=None):
    """
    Function that deletes a place
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Function that creates a place
    """
    city_obj = storage.get("City", city_id)
    obj_request = request.get_json()
    try:
        if city_obj is None:
            abort(404)
        if obj_request is None:
            abort(400, "Not a JSON")
        if 'user_id' not in obj_request:
            abort(400, "Missing user_id")
        if 'name' not in obj_request:
            abort(400, "Missing name")
        if 'description' not in obj_request:
            abort(400, "Missing description")
        user_obj = storage.get("User", obj_request['user_id'])
        if user_obj is None:
            abort(404)
        place_obj = Place(**obj_request)
        place_obj.city_id = city_obj.id
        place_obj.user_id = user_obj.id
        storage.new(place_obj)
        storage.save()
        return jsonify(place_obj.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def updates_place(place_id):
    """
    Function that updates a place
    """
    place_obj = storage.get("Place", place_id)
    obj_request = request.get_json()
    if place_obj is None:
        abort(404)
    if obj_request is None:
        abort(400, "Not a JSON")
    if 'user_id' in obj_request:
        user_obj = storage.get("User", obj_request['user_id'])
        if user_obj is None:
            abort(404)
        place_obj.user_id = user_obj.id
    if 'name' in obj_request:
        place_obj.name = obj_request['name']
    if 'description' in obj_request:
        place_obj.description = obj_request['description']
    if 'city_id' in obj_request:
        city_obj = storage.get("City", obj_request['city_id'])
        if city_obj is None:
            abort(404)
        place_obj.city_id = city_obj.id
    if 'number_rooms' in obj_request:
        place_obj.number_rooms = obj_request['number_rooms']
    if 'number_bathrooms' in obj_request:
        place_obj.number_bathrooms = obj_request['number_bathrooms']
    if 'max_guest' in obj_request:
        place_obj.max_guest = obj_request['max_guest']
    if 'price_by_night' in obj_request:
        place_obj.price_by_night = obj_request['price_by_night']
    if 'latitude' in obj_request:
        place_obj.latitude = obj_request['latitude']
    if 'longitude' in obj_request:
        place_obj.longitude = obj_request['longitude']
    if 'amenity_ids' in obj_request:
        for amenity_id in obj_request['amenity_ids']:
            amenity_obj = storage.get("Amenity", amenity_id)
            if amenity_obj is None:
                abort(404)
            place_obj.amenities.append(amenity_obj)
    storage.save()
    return jsonify(place_obj.to_dict()), 200




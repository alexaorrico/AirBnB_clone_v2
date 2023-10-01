#!/usr/bin/python3
"""Cities API actions"""

from flask import Flask, jsonify
from flask import abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """retrieve a list of all cities"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """CIty objects based on city id, else 404"""
    place = storage.get("Place", place_id)
    if place:
        result = place.to_dict()
        return jsonify(result)
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ CIty objects based on city id, else 404"""
    place = storage.get("Place", place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """CIty objects based on state id, else 404"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities
                if obj.id == city_id]
    if city_obj == []:
        abort(404)
    places = []
    new_place = Place(name=request.json['name'],
                      user_id=request.json['user_id'], city_id=city_id)
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users
                if obj.id == new_place.user_id]
    if user_obj == []:
        abort(404)
    storage.new(new_place)
    storage.save()
    places.append(new_place.to_dict())
    return jsonify(places[0]), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ CIty objects based on city id, else 404"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    update = request.get_json()
    if not update:
        abort(400, "Not a JSON")

    keys_to_exclude = ["id", "city_id", "user_id", "created_at", "updated_at"]
    for key in keys_to_exclude:
        update.pop(key, None)

    for key, value in update.items():
        setattr(place, key, value)

    storage.save()
    result = place.to_dict()
    return make_response(jsonify(result), 200)


@app_views.route("/places_search", methods=['POST'], strict_slashes=False)
def search_places():
    """Search for places based on JSON criteria"""
    criteria = request.get_json()
    if not criteria:
        abort(400, 'Not a JSON')

    states = criteria.get('states', [])
    cities = criteria.get('cities', [])
    amenities = criteria.get('amenities', [])

    places = []

    if not states and not cities and not amenities:
        places = storage.all("Place").values()
    else:
        for state_id in states:
            state = storage.get("State", state_id)
            if state:
                places.extend(state.places)
        for city_id in cities:
            city = storage.get("City", city_id)
            if city:
                places.extend(city.places)

        if amenities:
            places = [place for place in places if all(
                amenity.id in [
                    a.id for a in place.amenities] for amenity in amenities)]

    return jsonify([place.to_dict() for place in places])

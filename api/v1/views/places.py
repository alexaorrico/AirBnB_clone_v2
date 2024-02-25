#!/usr/bin/python3
"""Defines all routes for the `Place` entity
"""
from flask import abort, jsonify, request
from api.v1.views import app_views, places_amenities
from models import storage, classes


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_places(city_id):
    """Returns all places linked to given city_id"""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        return abort(404)
    places = city_obj.places
    if places is None:
        return abort(404)
    place_objs = []
    for place in places:
        place_objs.append(place.to_dict())
    return jsonify(place_objs)


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """Returns place with given place_id"""
    place = storage.get("Place", place_id)
    if place is None:
        return abort(404)
    return jsonify(place.to_dict())


@app_views.route("cities/<city_id>/places/", methods=["POST"])
def create_place(city_id):
    """Creates a new place in storage"""
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, description="Not a JSON")
    if "name" not in data:
        return abort(400, description="Missing name")
    if "user_id" not in data:
        return abort(400, description="Missing user_id")

    city = storage.get("City", city_id)
    user = storage.get("User", data.get("user_id"))
    if city is None or user is None:
        return abort(404)

    place = classes["Place"](**data)
    city.places.append(place)
    city.save()
    delattr(place, "cities")
    delattr(place, "user")
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Deletes a place object from storage"""
    place = storage.get("Place", place_id)
    if place is None:
        return abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """Update a place object by id"""
    place = storage.get("Place", place_id)
    if place is None:
        return abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, description="Not a JSON")

    data.pop("id", None)
    data.pop("user_id", None)
    data.pop("city_id", None)
    data.pop("updated_at", None)
    data.pop("created_at", None)

    for k, v in data.items():
        setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict())


@app_views.route("/places_search", methods=["POST"])
def places_search():
    """Filter place results by search keys in json body"""
    body = request.get_json(silent=True)
    if body is None:
        return abort(400, description="Not a JSON")
    if len(body) == 0 or not any(body.values()):
        all_places = storage.all("Place")
        if all_places is None:
            return jsonify([])
        return jsonify([place.to_dict() for place in all_places.values()])

    state_ids = body.get("states", [])
    city_ids = body.get("cities", [])
    amenity_ids = body.get("amenities", [])
    total_places = {}

    for state_id in state_ids:
        state = storage.get("State", state_id)
        if state is None:
            continue
        for city in state.cities:
            if city is None:
                continue
            for place in city.places:
                total_places[place.id] = place
    for city_id in city_ids:
        city = storage.get("City", city_id)
        if city is None:
            continue
        for place in city.places:
            total_places[place.id] = place

    if len(total_places) == 0:
        total_places = storage.all("Place")
    filtered_places = filter_places(total_places, amenity_ids)
    return jsonify(filtered_places)


def filter_places(places, amenity_ids):
    """Filter place record exclusively by amenity_ids"""
    filtered_places = []
    for pl in places.values():
        missing_amenity = False
        place_amenity_ids = [am.id for am in pl.amenities]
        for amenity_id in amenity_ids:
            if amenity_id not in place_amenity_ids:
                missing_amenity = True
                break
        if missing_amenity is False:
            delattr(pl, "amenities")
            filtered_places.append(pl.to_dict())
    return filtered_places

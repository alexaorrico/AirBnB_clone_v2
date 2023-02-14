#!/usr/bin/python3
"""Module for City related endpoints"""
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, make_response, abort, request
from models import storage
from models.place import Place

model = "Place"
parent_model = "City"


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["GET"])
def get_places(city_id):
    """GET /city api route"""
    return get_models(parent_model, city_id, "places")


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["GET"])
def get_place(place_id):
    """GET /place api route"""
    return get_model(model, place_id)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_place(place_id):
    """DELETE /place api route"""
    return delete_model(model, place_id)


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["POST"])
def post_place(city_id):
    """POST /places api route"""
    required_data = {"name", "user_id"}
    return post_model(model, parent_model, city_id, required_data)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["PUT"])
def put_place(place_id):
    """PUT /places api route"""
    ignore_data = ["id", "created_at", "updated_at", "user_id", "city_id"]
    return put_model(model, place_id, ignore_data)


@app_views.route("/places_search", strict_slashes=False,
                 methods=["POST"])
def search_places():
    """search for request places in database"""
    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, 'Not a JSON')

    ok = {"states", "cities"}
    places = []
    if not len(data) or all([len(v) == 0 for k, v in data.items() if k in ok]):
        places = storage.all("Place").values()

    if len(data.get("states", [])):
        states = [storage.get("State", id) for id in data["states"]]
        [[[places.append(place) for place in city.places]
         for city in state.cities] for state in states if state]

    if len(data.get("cities", [])):
        cities = [storage.get("City", id) for id in data["cities"]]
        [[places.append(place) for place in city.places]
         for city in cities if city]

    places = list(set(places))
    if len(data.get("amenities", [])):
        amenities = [storage.get("Amenity", id) for id in data["amenities"]]
        places = [place for place in places
                  if all([a in place.amenities for a in amenities])]

    return jsonify([place.to_dict() for place in places])

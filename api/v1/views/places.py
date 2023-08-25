#!/usr/bin/python3
"""Flask application for Place class/entity"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from flask import jsonify, abort, request


@app_views.routes("/cities/<city_id>/places",
                  methods=["GET"], strict_slashes=False)
def retrieves_all_places(city_id):
    """Returns the list of all Place objects"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = city.places
    places_dictionary = []
    for place in places:
        places_dictionary.append(place.to_dict)
    return jsonify(places_dictionary)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_places(place_id):
    """Returns an object by id"""
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    return jsonify(places.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def deletes_places(place_id):
    """Deletes an object by id"""
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    storage.delete(places)
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def create_places(city_id):
    """Creates a Place"""
    place_data = request.get_json()
    city = storage.get(City, city_id)
    user = storage.get(User, place_data.get("user_id"))
    if not city:
        abort(404)
    elif not place_data:
        abort(400, "Not a JSON")
    elif "user_id" not in place_data.keys():
        abort(400, "Missing user_id")
    elif not user:
        abort(404)
    elif "name" not in place_data.keys():
        abort(404,  "Missing name")

    place_data["city_id"] = city_id
    place = Place(**place_data)
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place_data = request.get_json()
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    elif not place_data:
        abort(400, "Not a JSON")

    for key, value in place_data.items():
        if key not in ["id", "state_id", "city_id",
                       "created_at", "updated_at"]:
            setattr(places, key, value)
    storage.save()
    return jsonify(places.to_dict()), 200

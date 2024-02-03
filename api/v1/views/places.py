#!/usr/bin/python3
"""Place RESTAPI"""
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_places(city_id):  # Get all places of a city
    city = storage.get(City, city_id)
    if city:
        return jsonify([place.to_dict() for place in city.places])
    abort(404)


@app_views.route("/places/<place_id>/", strict_slashes=False)
def get_place(place_id):  # get a specific place
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route("/places/<place_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_place(place_id):  # Delete a place
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=["POST"])
def create_place(city_id):  # Create a city in a place
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
    user = storage.get(User, data.get('user_id'))
    if not user:
        abort(404)
    data["city_id"] = city_id
    new_place = Place(**data)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["PUT"])
def update_place(place_id):  # Update a place
    place = storage.get(Place, place_id)
    if place:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        ignorables = ["id", "created_at", "updated_at", "user_id", "city_id"]
        for key, value in data.items():
            if key not in ignorables:
                setattr(place, key, value)
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)
    abort(404)

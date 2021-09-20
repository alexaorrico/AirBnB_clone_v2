#!/usr/bin/python3
"""module for places view"""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response

@app_views.route("/cities/<string:city_id>/places", strict_slashes=False, methods=["GET"])
def get_city_places(city_id):
    """retrives places"""
    required_city = storage.get(City, city_id)
    if (not required_city):
        abort(404)
    result = []
    for place in required_city.places:
        result.append(place.to_dict())
    return jsonify(result)


@app_views.route("/places/<string:place_id>", strict_slashes=False, methods=["GET"])
def get_place(place_id):
    """retrives a place"""
    required_place = storage.get(Place, place_id)
    if (not required_place):
        abort(404)
    return jsonify(required_place.to_dict())


@app_views.route("/places/<string:place_id>", strict_slashes=False, methods=["DELETE"])
def delete_place(place_id):
    """deletes a place"""
    required_place = storage.get(Place, place_id)
    if (not required_place):
        abort(404)
    storage.delete(required_place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<string:city_id>/places", strict_slashes=False, methods=["POST"])
def create_place(city_id):
    """creates a new place"""
    required_city = storage.get(City, city_id)
    if (not required_city):
        abort(404)
    if not request.json:
        return make_response("Not a JSON", 400)
    if not 'user_id' in request.json:
        return make_response("Missing user_id", 400)

    properties = request.get_json()
    required_user = storage.get(User, properties["user_id"])
    if (not required_user):
        abort(404)

    if not 'name' in request.json:
        return make_response("Missing name", 400)
    new_place = Place(**properties)
    new_place.save()
    return new_place.to_dict(), 201


@app_views.route("/places/<string:place_id>", strict_slashes=False, methods=["PUT"])
def edit_place(place_id):
    """edits a place"""
    required_place = storage.get(Place, place_id)
    if (not required_place):
        abort(404)
    if not request.json:
        return make_response("Not a JSON", 400)

    input_dict = request.get_json()
    for key, value in input_dict.items():
        if not (key in ["id", "created_at", "updated_at", "user_id", "city_id"]):
            if (hasattr(required_place, key)):
                setattr(required_place, key, value)
    required_place.save()
    return required_place.to_dict(), 200

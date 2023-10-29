#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from flasgger.utils import swag_from
from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def get_place_cities(city_id):
    """return a list of places in the city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place = city.places
    if not place:
        abort(404)
    else:
        return jsonify([cit.to_dict() for cit in place])


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
@swag_from("documentation/place/get_id.yml", methods=["GET"])
def get_place_id(place_id):
    """Retrieves a specific place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<string:place_id>", methods=["DELETE"], strict_slashes=False)
@swag_from("documentation/place/delete.yml", methods=["DELETE"])
def delete_place(place_id):
    """Deletes a  place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
@swag_from("documentation/city/post_city.yml", methods=["POST"])
def post_city(city_id):
    """
    Creates a City object
    """
    if not storage.get(City, city_id):
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    if "user_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    if not storage.get(User, body.user_id):
        abort(404)

    body = request.get_json()
    instance = Place(**body)
    instance.city_id = city_id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
@swag_from("documentation/place/put_place.yml", methods=["PUT"])
def put_place(place_id):
    """put place change the values of the place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, val in dict(request.get_json()).items():
        setattr(place, key, val)

    storage.save()

    return jsonify(place.to_dict())

#!/usr/bin/python3
"""Module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from flask import make_response, abort, request
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def places_of_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    list_places = []
    for place in city.places:
        list_places.append(place.to_dict())

    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def places_id(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "user_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    req_body = request.get_json()
    user_id = req_body.get("user_id")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if "name" not in req_body:
        return make_response(jsonify({"error": "Missing name"}), 400)

    req_body["city_id"] = city.id
    req_body["user_id"] = user.id
    object = Place(**req_body)
    storage.new(object)
    storage.save()
    return make_response(jsonify(object.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    req_body = request.get_json()
    exempt = ["id", "user_id", "city_id" "created_at", "updated_at"]

    for key, value in req_body.items():
        if key not in exempt:
            setattr(place, key, value)
        else:
            pass

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)

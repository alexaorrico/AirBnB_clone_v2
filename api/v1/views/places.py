#!/usr/bin/python3
"""Module for place endpoints"""
from flask import jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_cities_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'])
def get_places(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("cities/<city_id>/places",
                 strict_slashes=False, methods=["POST"])
def post_place(city_id):
    """POST /city API route"""
    city = storage.get(City, city_id)
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)

    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    if "user_id" not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    user = storage.get(User, data["user_id"])
    if not user:
        return make_response(jsonify({"error": "Not found"}), 404)

    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"])
def put_place(place_id):
    """PUT /city API route"""
    place = storage.get(Place, place_id)
    if not place:
        return make_response(jsonify({"error": "Not found"}), 404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)

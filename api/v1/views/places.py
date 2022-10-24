#!/usr/bin/python3
"""route for places"""
from api.v1.views import app_views
from models.city import City
from models import storage
from models.place import Place
from models.user import User
from flask import jsonify, abort, request, make_response


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["GET"])
def get_places(city_id):
    """get the places in a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    all_places = []
    for place in city.places:
        all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["GET"])
def a_place(place_id):
    """retrieves a place"""
    if request.method == "GET":
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_place(place_id):
    """deletes a place"""
    if request.method == "DELETE":
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["POST"])
def post_place(city_id):
    """post/create a place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if not storage.get(User, data['user_id']):
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")
    place = Place(**data)
    place.city_id = city.id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["PUT"])
def put_place(place_id):
    """updates a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignores = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for attr, val in data.items():
        if attr not in ignores:
            setattr(place, attr, val)
    place.save()
    return jsonify(place.to_dict()), 200

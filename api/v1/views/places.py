#!/usr/bin/python3
""" Methos API for object Place """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models import place
from models.city import City
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_city_place(city_id):
    """ Get one Places objects of City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """ Get one Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Delete a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ Create a new Place object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    request_place = request.get_json()
    if not request_place:
        abort(400, "Not a JSON")
    if "user_id" not in request_place:
        abort(400, "Missing user_id")
    user_id = request_place['user_id']
    if not storage.get("User", user_id):
        abort(404)
    if "name" not in request_place:
        abort(400, "Missing name")
    place = Place(**request_place)
    place.city_id = city_id
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """ Update a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    request_place = request.get_json()
    if not request_place:
        abort(400, "Not a JSON")

    for key, value in request_place.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)

#!/usr/bin/python3
""" Module for place object view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Returns all place objects """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    places_dict_list = [place.to_dict() for place in city.places]
    return jsonify(places_dict_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_id(place_id):
    """ Method retrieves place object with certain id """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Method deletes place object based off of its id """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ Method creates new place object """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if body.get("user_id") is None:
        abort(400, "Missing user_id")
    if body.get("name") is None:
        abort(400, "Missing name")
    user = storage.get("User", body['user_id'])
    if not user:
        abort(404)
    body['city_id'] = city_id
    place = Place(**body)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """ Method updates a place object based off its id """
    place = storage.get("Place", place_id)
    body = request.get_json()
    if not place:
        abort(404)
    if not body:
        abort(400, "Not a JSON")
    for k, v in body.items():
        if k not in ["id", "user_id", "city_id",
                     "created_at", "updated_at"]:
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict())

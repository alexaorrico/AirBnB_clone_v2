#!/usr/bin/python3

"""places view module"""

from api.v1.views import app_views
from models.place import Place
from models.city import City
from flask import jsonify, abort, request
import models


@app_views.route('/cities/<city_id>/places', methods=["GET"], strict_slashes=False)
def places(city_id):
    """return all the places"""
    cities = models.storage.get(City, city_id)
    if city_id is None:
        return abort(404)
    if cities is None:
        return abort(404)
    return jsonify([place.to_dict() for place in cities.places])


@app_views.route('/places/<place_id>', methods=["GET"], strict_slashes=False)
def get_place_by_id(place_id):
    """return a by id or 404"""
    place = models.storage.get(Place, place_id)
    if place_id is None:
        return abort(404)
    if place is None:
        return abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """delete place data by id"""
    place = models.storage.get(Place, place_id)
    if place_id is None:
        return abort(404)
    if place is None:
        return abort(404)
    else:
        models.storage.delete(place)
        return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def add_place(city_id):
    """add new place"""
    try:
        req_data = request.get_json(force=True)
    except Exception:
        req_data = None
    if city_id is None:
        return abort(404)
    city = models.storage.get(City, city_id)
    if city is None:
        return abort(404)
    if req_data is None:
        return "Not a JSON", 400

    if "name" not in req_data.keys():
        return "Missing name", 400

    new_place = Place(req_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """update place object"""
    try:
        req_data = request.get_json(force=True)
    except Exception:
        return "Not a JSON", 400
    place = models.storage.get(Place, place_id)
    if place is None:
        return abort(404)
    for key in ("id", "created_at", "updated_at","user_id", "city_id"):
        req_data.pop(key, None)
    for k, v in req_data.items():
        setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200

#!/usr/bin/python3
""" Places """
import json
from models import storage
from flask import jsonify, abort, request, make_response
from models.city import City
from models.place import Place
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id):
    """ DO some method on City with a city_id """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        list_places = []
        for place in city.places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    if request.method == 'POST':
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        if response.get("name") is None:
            abort(400, "Missing name")
        if response.get("user_id") is None:
            abort(400, "Missing user_id")

        new = Place(**response)
        new.city_id = city.id
        new.save()
        return make_response(jsonify(new.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_id(place_id):
    """ Do different methods on a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({})

    elif request.method == 'PUT':
        ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        for key, value in response.items():
            if key not in ignore:
                setattr(place, key, value)
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)

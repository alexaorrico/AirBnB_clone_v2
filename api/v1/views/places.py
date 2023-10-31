#!/usr/bin/python3
"""Flask route for place model"""

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.place import Place
from models.city import City
from os import environ
STOR_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places(city_id=None):
    """route to return all cities"""

    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404, 'Not found')

    if request.method == "GET":
        places_dict = storage.all(Place)
        places_list = [obj.to_dict()
                       for obj in places_dict.values()
                       if obj.city_id == city_id
                       ]
        return jsonify(places_list)

    if request.method == "POST":
        request_json = request.get_json()
        if request_json is None:
            abort(400, "Not a JSON")
        if request_json.get("user_id") is None:
            abort(400, "Missing user_id")
        if storage.get("User", request_json.get("user_id")) is None:
            abort(404, "Not found")
        if request_json.get("name") is None:
            abort(400, "Missing name")

        request_json["city_id"] = city_id
        newPlace = Place(**request_json)
        newPlace.save()
        return make_response(jsonify(newPlace.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"])
def place(place_id=None):
    """Get, update or delete place with place id"""
    place_obj = storage.get(Place, place_id)

    if place_obj is None:
        abort(404, "Not found")

    if request.method == "GET":
        return jsonify(place_obj.to_dict())

    if request.method == "DELETE":
        place_obj.delete()
        storage.save()
        return jsonify({})

    if request.method == "PUT":
        request_json = request.get_json()
        if request_json is None:
            abort(400, "Not a JSON")
        place_obj.update(request_json)
        return make_response(jsonify(place_obj.to_dict()), 200)

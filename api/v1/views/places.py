#!/usr/bin/python3
""" Places """

from flask import jsonify, request, abort
from models.place import Place
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=["GET", "POST"],
                 strict_slashes=False)
def list_places(city_id):
    """ Retrieves the list of all Places objects """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        places = storage.all("Place")
        all_places = []
        for key in places.values():
            if key.city_id == city_id:
                all_places.append(key.to_dict())
        return jsonify(all_places)
    if request.method == "POST":
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        if "user_id" not in response:
            abort(400, "Missing user_id")
        user = storage.get("User", response["user_id"])
        if user is None:
            abort(404)
        if "name" not in response:
            abort(400, "Missing name")
        response["city_id"] = city_id
        new_place = Place(**response)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def place(place_id):
    """ Manipulate an specific Place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict())
    if request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        for key, value in response.items():
            if key not in ['id', 'created_at', 'updated_at', 'user_id',
                           'city_id']:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200

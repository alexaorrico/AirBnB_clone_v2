#!/usr/bin/python3
"""Place view"""


from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=["GET", "POST"], strict_slashes=False)
def places(city_id):
    """retrieve or create places depending on request method"""
    if request.method == "GET":
        places = []
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        for place in city.places:
            places.append(place.to_dict())
        places_json = jsonify(places)
        return places_json
    elif request.method == "POST":
        place_dict = request.get_json()
        if place_dict is None:
            abort(400, "Not a JSON")

        place_user_id = place_dict.get("user_id")
        if place_user_id is None:
            abort(400, "Missing user_id")
        if "name" not in place_dict:
            abort(400, "Missing name")
        user = storage.get(User, place_user_id)
        city = city = storage.get(City, city_id)
        if user is None or city is None:
            abort(404)
        place_dict["city_id"] = city_id
        new_place = Place(**place_dict)
        new_place.save()
        new_place_json = jsonify(new_place.to_dict())
        return new_place_json, 201


@app_views.route('/places/<place_id>', methods=["GET"],
                 strict_slashes=False)
def places_id(place_id):
    """retrieve place with id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_json = jsonify(place.to_dict())
    return place_json


@app_views.route('/places/<place_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """delete an place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """update an place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_dict = request.get_json()
    if place_dict is None:
        abort(400, "Not a JSON")
    for k, v in place_dict.items():
        if k not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(place, k, v)
    place.save()
    place_json = jsonify(place.to_dict())
    return place_json, 200

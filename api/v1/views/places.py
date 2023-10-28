#!/usr/bin/python3
"""this view hundles states endpoints"""
from flask import abort
from api.v1.views import app_views
from flask import jsonify
from flask import request
from models.place import Place
from models.city import City
from models.state import State
from models.user import User
from models.amenity import Amenity
from models import storage


@app_views.route("/cities/<city_id>/places", methods=["POST", "GET"],
                 strict_slashes=False)
def all_place_for_city(city_id):
    """gets all cities instances"""
    if request.method == "GET":

        d_cities = storage.all(City)
        try:
            key = "City." + city_id
            city = d_cities[key]
            list_place = [place.to_dict() for place in city.places]
            return jsonify(list_place)
        except KeyError:
            abort(404)
    elif request.method == "POST":
        d_cities = storage.all(City)

        if ("City." + city_id) not in d_cities:
            abort(404)
        if request.is_json:
            data = request.get_json()
        else:
            abort(400, "Not a JSON")

        if "user_id" not in data:
            abort(400, "Missing user_id")
        if "name" not in data:
            abort(400, "Missing name")

        users = storage.all(User)
        if ("User." + data["user_id"]) not in users.keys():
            abort(404)

        data.update({"city_id": city_id})
        new = Place(**data)
        storage.new(new)
        storage.save()
        return jsonify(new.to_dict()), 201
    else:
        abort(501)


@app_views.route("/places/<place_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def work_place(place_id=None):
    """working with places"""
    if request.method == "GET":
        places = storage.all(Place)
        try:
            key = "Place." + place_id
            place = place[key]
            return jsonify(place.to_dict())
        except KeyError:
            abort(404)
    elif request.method == "PUT":
        d_places = storage.all("Place")
        key = "Place." + place_id
        try:
            place = d_places[key]
            if request.is_json:
                data = request.get_json()
            else:
                abort(400, "Not a JSON")
            bad_tag = ["id", "user_id", "city_id", "created_at", "updated_at"]
            for k, v in data.items():
                if key not in bad_tag:
                    setattr(place, k, v)
            storage.save()
            return jsonify(place.to_dict()), 200
        except KeyError:
            abort(404)
        else:
            abort(501)
    elif request.method == "DELETE":
        d_places = storage.all(Place)
        try:
            key = "Place." + place_id
            storage.delete(d_places[key])
            storage.save()
            return jsonify({}), 200
        except KeyError:
            abort(404)

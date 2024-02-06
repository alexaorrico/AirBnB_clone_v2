#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.user import User
from models.city import City
from models.place import Place
from models.base_model import BaseModel

@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"],
                    strict_slashes=False)
def get_place(city_id):
    res = []
    city = storage.get(City, city_id)
    if request.method == "GET":
        places = storage.all(Place).values()
        for place in city.places:
            res.append(place.to_dict())
            return (jsonify(res))
            if request.method == "POST":
                if not request.json:
                    abort(400, description="Not a JSON")
                if "user_id" not in request.json:
                    abort(400, description="Missing user_id")
                if "name" not in request.json:
                    abort(400, description="Missing name")
                new_place = Place(**request.json)
                new_place.city_id = city_id
                new_place.save()
                return (jsonify(new_place.to_dict()), 201)

@app_views.route("/places/<place_id>", methods=[
                "GET", "PUT", "DELETE"], strict_slashes=True)
def manage_place(place_id):
    Place = storage.get(Place, place_id)
    if Place is None:
        abort(404)
    if request.method == "GET":
        return jsonify(Place.to_dict())
    if request.method == "PUT":
        if not request.json:
            abort(400, description="Not a JSON")
            for key, value in request.json.items():
                setattr(Place, key, value)
            Place.save()
            return (jsonify(Place.to_dict()), 200)
    if request.method == "DELETE":
        storage.delete(Place)
        storage.save()
        return make_response(jsonify({}), 200)
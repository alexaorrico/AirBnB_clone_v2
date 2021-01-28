#!/usr/bin/python3
"""this is a test string"""

from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route("/cities/<c_id>/places",
                 strict_slashes=False,
                 methods=["GET", "POST"])
def places_base(c_id):
    """this is a test string"""
    if request.method == "GET":
        out = []
        city = storage.get(City, c_id)
        if city:
            for place in city.places:
                out.append(place.to_dict())
            return jsonify(out)
        abort(404)
    if request.method == "POST":
        if not request.is_json:
            return "Not a JSON", 400
        city = storage.get(City, c_id)
        if city:
            kwargs = {"city_id": c_id}
            kwargs.update(request.get_json())
            out = Place(**kwargs)
            info = out.to_dict()
            if "user_id" not in info.keys():
                return "Missing user_id", 400
            if not storage.get(User, info.get("user_id")):
                abort(404)
            if "name" not in info.keys():
                return "Missing name", 400
            out.save()
            return out.to_dict(), 201
        abort(404)


@app_views.route("/places/<p_id>",
                 strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def places_id(p_id):
    """this is a test string"""
    if request.method == "GET":
        place = storage.get(Place, p_id)
        if place:
            return place.to_dict()
        abort(404)
    if request.method == "DELETE":
        place = storage.get(Place, p_id)
        if place:
            place.delete()
            storage.save()
            return {}, 200
        abort(404)
    if request.method == "PUT":
        place = storage.get(Place, p_id)
        if place:
            if not request.is_json:
                return "Not a JSON", 400
            for k, v in request.get_json().items():
                if k not in ["id", "user_id", "city_id",
                             "created_at", "updated_at"]:
                    setattr(place, k, v)
            storage.save()
            return place.to_dict(), 200
        abort(404)

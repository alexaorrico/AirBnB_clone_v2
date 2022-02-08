#!/usr/bin/python3
"""palce"""

from crypt import methods
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models import storage
from sqlalchemy.exc import IntegrityError


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places(city_id=None):
    """retrieves the list of all City objects"""
    all_places = []
    city_obj = storage.get("City", city_id)
    if city_obj:
        for place_obj in city_obj.places:
            all_places.append(place_obj.to_dict())
        return jsonify(all_places)
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id=None):
    """retrieves a Place object"""
    place_obj = storage.get("Place", place_id)
    if place_obj:
        return jsonify(place_obj.to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """deletes a Place object"""
    place_obj = storage.get("Place", place_id)
    if place_obj:
        storage.delete(place_obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates a city object"""
    city_obj = storage.get("City", city_id)
    obj_request = request.get_json()
    try:
        if city_obj:
            if obj_request:
                if 'name' in obj_request and 'user_id' in obj_request:
                    new_place_obj = Place(**obj_request)
                    setattr(new_place_obj, "city_id", city_id)
                    new_place_obj.save()
                    return (jsonify(new_place_obj.to_dict()), 201)
                else:
                    if 'user_id' not in obj_request:
                        abort(400, "Missing user_id")
                    if 'name' not in obj_request:
                        abort(400, "Missing name")
            else:
                abort(400, "Not a JSON")
        else:
            abort(404)
    except IntegrityError:
        abort(404)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """updates a city object"""
    place_onj = storage.get(Place, place_id)
    obj_request = request.get_json()
    if place_onj:
        if obj_request:
            if 'name' in obj_request:
                for key, value in obj_request.items():
                    ignore = ["id", "user_id", "city_id",
                              "created_at", "updated_at"]
                    if key != ignore:
                        setattr(place_onj, key, value)
                place_onj.save()
                return jsonify(place_onj.to_dict()), 200
            else:
                return "Missing name", 400
        else:
            return "Not a JSON", 400
    else:
        abort(404)

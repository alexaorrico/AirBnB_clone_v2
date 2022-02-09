#!/usr/bin/python3
"""
Methods for places RESTFul
"""

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"],
                 strict_slashes=False)
def get_allplaces(city_id=None):
    """ List all cities """
    get_cities = storage.get("City", city_id)
    list_places = []
    if get_cities:
        all_places = storage.all("Place").values()
        for element in all_places:
            if element.city_id == str(city_id):
                list_places.append(element.to_dict())
        return jsonify(list_places)
    else:
        abort(404)


@app_views.route("/places/<place_id>",
                 methods=["GET"],
                 strict_slashes=False)
def get_id_place(place_id=None):
    """ Return Place """
    places = storage.get(Place, place_id)
    if places:
        return jsonify(places.to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def id_place(place_id):
    """ Return id delete"""
    dict_place = storage.get(Place, place_id)
    if dict_place:
        storage.delete(dict_place)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"],
                 strict_slashes=False)
def post_places(city_id=None):
    """ Create a new place """
    data = request.get_json()
    list_places = []
    places_ob = storage.get("City", city_id)
    if places_ob:
        if data:
            if "name" in data and "user_id" in data:
                new_place = Place(**data)
                setattr(new_place, "city_id", city_id)
                new_place.save()
                return jsonify(new_place.to_dict(), 201)
            else:
                abort("Missing user_id", 400)
        else:
            abort("Not a JSON", 400)
    else:
        abort(404)


@app_views.route("/places/<place_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def put_place(place_id):
    """ Update Place item """
    up_date = storage.get(Place, place_id)
    place_ob = request.get_json()
    if up_date:
        if place_ob:
            ignore = ["id", "state_id", "created_at", "updated_at"]
            for k, v in place_ob.items():
                if k not in ignore:
                    setattr(up_date, k, v)
            storage.save()
            return jsonify(up_date.to_dict()), 200
        else:
            return"Not a JSON", 400
    else:
        abort(404)

#!/usr/bin/python3
"""Handles all default RestFul API actions for State objects"""

from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places",
                 methods=['GET', 'POST'],
                 strict_slashes=False)
@app_views.route("/places/<place_id>",
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def cities_places_list(city_id=None, place_id=None):
    """Retrieves a list of all Place objects derived from City IDs"""
    if request.method == 'GET':
        l_1 = []
        if city_id and not place_id:
            city = storage.get("City", city_id)
            if not city:
                abort(404)
            for value in city.places:
                d = value.to_dict()
                l_1.append(d)
            return jsonify(l_1)
        elif place_id and not city_id:
            place = storage.get("Place", place_id)
            if not place:
                abort(404)
            return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        place = storage.get("Place", place_id)
        if not place:
            abort(404)
        place.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'POST':
        city = storage.get("City", city_id)
        if not city:
            abort(404)
        dic = request.get_json()
        if not dic:
            return 'Not a JSON', 400
        if "user_id" not in dic.keys():
            return 'Missing user_id', 400
        user = storage.get("User", dic["user_id"])
        if not user:
            abort(404)
        if "name" not in dic.keys():
            return 'Missing name', 400
        dic.update(city_id=city_id)
        p = Place(**dic)
        p.save()
        return jsonify(p.to_dict()), 201
    elif request.method == 'PUT':
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        dic = request.get_json()
        if not dic:
            return 'Not a JSON', 400
        for k, v in dic.items():
            if (k != "id" or k != "created_at" or k != "updated_at" or
                    k != "city_id" or k != "user_id"):
                setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict()), 200

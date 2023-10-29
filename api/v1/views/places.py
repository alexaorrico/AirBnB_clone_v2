#!/usr/bin/python3
"""
place
"""

from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route('/cities/<string:id>/places', methods=["GET"])
def places_by_city(id):
    """GET Place by city id"""
    city = storage.get(City, id)
    if city is None:
        abort(404)
    if city.places is None:
        abort(404)
    else:
        places = city.places
        places_list = []
        for place in places:
            places_list.append(place.to_dict())
    return (jsonify(places_list))


@app_views.route('/places/<string:id>', methods=["GET"])
def place(id):
    """GET Place by id"""
    place = storage.get(Place, id)
    if place is None:
        abort(404)
    return (jsonify(place.to_dict()))


@app_views.route('/places/<string:id>', methods=["DELETE"])
def remove_place(id):
    """REMOVE place by id"""
    place = storage.get(Place, id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return {}, 200


@app_views.route('/cities/<string:id>/places/', methods=["POST"])
def create_place(id):
    """CREATE place by city id"""
    if request.is_json:
        json_place = request.get_json()
        if json_place.get("name") is None:
            abort(400, description="Missing name")
        if json_place.get("user_id") is None:
            abort(400, description="Missing user_id")
        else:
            if storage.get(City, id) is None:
                abort(404)
            json_place["city_id"] = id
            new_place = Place(**json_place)
            storage.new(new_place)
            storage.save()
            return new_place.to_dict(), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/places/<string:id>', methods=["PUT"])
def update_place(id):
    """UPDATE Place by id"""
    place = storage.get(Place, id)
    if place is None:
        abort(404)
    if request.is_json:
        forbidden = ["id", "created_at", "updated_at", "user_id",
                     "city_id"]
        # user = storage.get(User, id)
        # if user is None:
        #     abort(404)
        json_place = request.get_json()
        # storage.delete(place)
        for k, v in json_place.items():
            if json_place[k] not in forbidden:
                setattr(place, k, v)
        # storage.new(place)
        storage.save()
        return place.to_dict(), 200
    else:
        abort(400, description="Not a JSON")

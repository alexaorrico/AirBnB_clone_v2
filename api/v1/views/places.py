#!/usr/bin/python3
""" index routes """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places")
def get_places(city_id):
    """get all places belong city"""
    res = storage.get(City, city_id)
    if res is None:
        abort(404)
    else:
        places = []
        for place in res.places:
            places.append(place.to_dict())
    return jsonify(places)


@app_views.route("/places/<place_id>")
def get_place(place_id):
    """get place"""
    res = storage.get(Place, place_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """delete place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """add new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.json is None:
        abort(400, "Not a JSON")
    data = request.get_json()
    if data.get('user_id') is None:
        return "Missing user_id", 400
    user = storage.get(User, data.get('user_id'))
    if user is None:
        abort(404)
    if data.get('name') is None:
        return "Missing name", 400
    data["city_id"] = city_id
    new_place = Place(name=request.json['name'])
    # new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """update place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if request.json is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200

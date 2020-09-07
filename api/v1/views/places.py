#!/usr/bin/python3
""" amenities view class """
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, request, abort, make_response


@app_views.route("/cities/<string:city_id>/places",
                 strict_slashes=False, methods=["GET", "POST"])
def get_place_fromcity(city_id=None):
    """ retrives all places from a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        return jsonify([place.to_dict() for place in city.places])
    if request.method == "POST":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if request.get_json().get("user_id") is None:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        if request.get_json().get("name") is None:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        user = storage.get(User, request.get_json().get("user_id"))
        if user is None:
            abort(404)
        dic = request.get_json()
        dic.update({"city_id": city_id})
        place = Place(**dic)
        place.save()
        return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<string:place_id>",
                 strict_slashes=False, methods=["GET", "DELETE", "PUT"])
def get_place_id(place_id=None):
    """ gets place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict())
    if request.method == "DELETE":
        place.delete()
        storage.save()
        return jsonify({})
    if request.method == "PUT":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, val in request.get_json().items():
            if key not in ['id', 'created_at',
                           'updated_at', 'user_id', 'city_id']:
                setattr(place, key, val)
        place.save()
        return jsonify(place.to_dict())

#!/usr/bin/python3
"""view for Place"""

from api.v1.views import *
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import *


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET', 'POST'])
def places_by_city(city_id):
    """Function that retrieve and save a new city"""
    places = storage.all('Place').values()
    city = storage.get(City, city_id)
    ls = []
    if city:
        for place in places:
            if place.city_id == city_id:
                ls.append(place.to_dict())
        if request.method == "GET":
            return jsonify(ls)
        elif request.method == "POST":
            if not request.json:
                return make_response(jsonify(
                                     {'error': "Not a JSON"}), 400)
            elif 'user_id' not in request.json:
                return make_response(jsonify(
                                     {'error': "Missing user_id"}), 400)
            elif 'name' not in request.json:
                return make_response(jsonify(
                                     {'error': "Missing name"}), 400)
            else:
                if storage.get(User, request.json['user_id']) is None:
                    abort(404)
                else:
                    json = request.json
                    json['city_id'] = city_id
                    new = Place(**json)
                    new.save()
                    return make_response(new.to_dict(), 201)
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def place(place_id):
    """Function that retrieve, delete and put a place"""
    place = storage.get(Place, place_id)
    if place:
        if request.method == "GET":
            return place.to_dict()
        elif request.method == "DELETE":
            storage.delete(place)
            storage.save()
            return {}
        elif request.method == "PUT":
            if not request.json:
                return make_response(jsonify({'error': "Not a JSON"}), 400)
            else:
                json = request.json
                for key, value in json.items():
                    if key != 'id' and key != 'user_id' and\
                       key != 'city_id' and key != 'created_at' and\
                       key != "updated_at":
                        setattr(place, key, value)
                place.updated_at = datetime.utcnow()
                storage.save()
                return make_response(place.to_dict(), 200)
    abort(404)

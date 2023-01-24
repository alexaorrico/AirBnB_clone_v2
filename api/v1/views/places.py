#!/usr/bin/python3
""" state view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.base_model import BaseModel


@app_views.route('/cities/<city_id>/places',
                 methods=["GET", "POST"], strict_slashes=False)
def get_places(city_id):
    """get all instances of places in a city"""
    response = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        for place in city.places:
            response.append(place.to_dict())
        return (jsonify(response))

    if request.method == "POST":
        """post a new instance"""
        new_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'user_id' not in request.json:
            abort(400, description="Missing user_id")
        user_id = new_data['user_id']
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        if 'name' not in request.json:
            abort(400, description="Missing name")
        new_data['city_id'] = city_id
        place = Place(**new_data)
        place.save()
        return (jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=["GET", "PUT"],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """get, update an instance of place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        response = place.to_dict()
        return (jsonify(response))
    if request.method == "PUT":
        new_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in new_data.items():
            setattr(place, key, value)
        place.save()
        return (jsonify(place.to_dict()), 200)


@app_views.route('/places/<place_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """delete an instance of place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "DELETE":
        storage.delete(place)
        storage.save()
        response = make_response(jsonify({}), 200)
        return response

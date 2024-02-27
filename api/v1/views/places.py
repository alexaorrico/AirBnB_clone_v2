#!/usr/bin/python3
"""
Gives another view for the places objects,
helps deal with the RESTful API
"""
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views
from models.user import User
from models.base_model import BaseModel


@app_views.route('/cities/<city_id>/places', methods=["GET", "POST"],
                 strict_slashes=False)
def get_city_places(city_id):
    """
    gets all place objs of a city
    """
    output_list = []
    defined_city = storage.get(City, city_id)
    if defined_city is None:
        abort(404)
    if request.method == "GET":
        for place in defined_city.places:
            output_list.append(place.to_dict())
        return (jsonify(output_list))
    if request.method == "POST":
        user_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'user_id' not in request.json:
            abort(400, description="Missing user_id")
        user_id = user_data['user_id']
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        if 'name' not in request.json:
            abort(400, description="Missing name")
        user_data['city_id'] = city_id
        place = Place(**user_data)
        place.save()
        return (jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=[
                 "GET", "PUT", "DELETE"], strict_slashes=False)
def get_single_place(place_id):
    """
    gets a single place depending on ID
    """
    defined_place = storage.get(Place, place_id)
    if defined_place is None:
        abort(404)
    if request.method == "GET":
        user_output = defined_place.to_dict()
        return (jsonify(user_output))
    if request.method == "PUT":
        user_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in user_data.items():
            setattr(defined_place, key, value)
        defined_place.save()
        return (jsonify(defined_place.to_dict()), 200)
    if request.method == "DELETE":
        storage.delete(defined_place)
        storage.save()
        worked_result = make_response(jsonify({}), 200)
        return worked_result

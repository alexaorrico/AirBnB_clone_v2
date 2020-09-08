#!/usr/bin/python3
""" place view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.place import Place
from models.base_model import BaseModel


@app_views.route('/places', methods=["GET"], strict_slashes=False)
def get_all_places():
    """ retrieves all place objects """
    output = []
    places = storage.all(Place).values()
    for place in places:
        output.append(place.to_dict())
    return (jsonify(output))


@app_views.route('/cities/<city_id>/places', methods=["GET", "POST"]
                 , strict_slashes=False)
def get_city_place():
    """ gets all place objs of a city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        for place in city.places:
            output.append(place.to_dict())
        return (jsonify(output))
    if request.method == "POST":
        request.get_json()
        if not request.is_json():
            abort(400, description="Not a JSON")
        if 'user_id' not in request.json():
            abort(400, description="Missing user_id")
        if 'name' not in request.json():
            abort(400, description="Missing name")
        user = User(**data)
        user.save()
        return (jsonify(user.to_dict()), 201)

@app_views.route('/places/<place_id>', methods=[
                 "GET", "PUT", "DELETE"], strict_slashes=False)
def get_a_place(place_id):
    """ retrieves one unique place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        output = place.to_dict()
        return (jsonify(output))
    if request.method == "PUT":
        data = request.get_json()
        if not request.is_json():
            abort(400, description="Not a JSON")
        for key, value in data.items():
            setattr(place, key, value)
        place.save()
        return (jsonify(place.to_dict()), 200)
    if request.method == "DELETE":
        storage.delete(place)
        storage.save()
        result = make_response(jsonify({}), 200)
        return result

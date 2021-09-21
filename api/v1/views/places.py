#!/usr/bin/python3
""" handles all default RESTFul API actions """
from os import abort
from models.place import Place
from flask.json import jsonify
from api.v1.views import app_views
from flask import request, abort
from models import storage


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def get_city(city_id=None):
    """
    Retrieves the list of all Place objects of a City:
        GET /api/v1/cities/<city_id>/places
    Retrieves a Place object:
        GET /api/v1/places/<place_id>
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404, 'Not found')
    if request.method == "GET":
        all_places = storage.all('Place')
        places = []
        for place in all_places.values():
            if place.city_id == city_id:
                places.append(place.to_dict())
        return jsonify(places)
    if request.method == "POST":
        json_req = request.get_json()
        if json_req is None:
            abort(400, 'Not a Json')
        if json_req.get("name") is None:
            abort(400, 'Missing name')
        if json_req.get("user_id") is None:
            abort(400, 'Missing user_id')
        json_req["city_id"] = city_id
        new_obj = Place(**json_req)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def CUD_place(place_id=None):
    """
    Deletes a Place object:
        GET /api/v1/places/<place_id>
    Creates a Place:
        POST /api/v1/cities/<city_id>/places
    Updates a Place object:
        PUT /api/v1/places/<place_id>
    """
    place = storage.get('Place', place_id)
    # no corresponding city was found
    if place is None:
        return "404 not found"
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == "DELETE":
        place.delete()
        return jsonify({}, 200)
    if request.method == 'PUT':
        print("HERE NOW")
        json_req = request.get_json()
        if json_req is None:
            abort(400, 'Not a JSON')
        place.update(json_req)
        return jsonify(place.to_dict()), 200

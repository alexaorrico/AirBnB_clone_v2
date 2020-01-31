#!/usr/bin/python3
""" Place Module"""


from models.place import Place
from models.city import City
from models import storage
from flask import Flask, abort, jsonify, request, json
from api.v1.views import app_views
import json


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """    Retrieves the list of all Place objects
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object by id
    """
    place = storage.get("Place", place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place():
    """
    Create a new Place instance
    """
    city = storage.get("City", city_id)
    error_message = ""
    if city:
        content = request.get_json(silent=True)
        if type(content) is dict:
            if "user_id" in content.keys():
                user = storage.get('User', content['user_id'])
                if user:
                    if "name" in content.keys():
                        place = Place(**content)
                        place.city_id = city_id
                        storage.new(place)
                        storage.save()
                        response = jsonify(place.to_dict())
                        response.status_code = 201
                        return response
                    else:
                        error_message = "Missing name"
                else:
                    abort(404)
            else:
                error_message = "Missing user_id"
        else:
            error_message = "Not a JSON"

        response = jsonify({"error": error_message})
        response.status_code = 400
        return response
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    Update a Place instance
    """
    if not request.json:
        abort(400, "Not a JSON")
    place = storage.get("Place", id=place_id)
    if place:
        place.name = request.json['name']
        place.save()
        return jsonify(place.to_dict()), 200
    abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Delete a Place instance
    """
    place = storage.get("Place", id=place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)

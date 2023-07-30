#!/usr/bin/python3
"""
A module that handles all default RESTFul API actions for places objects
"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """ Retrieves a list of all places """
    city_obj = storage.get("City", city_id)
    if not city_obj:
        abort(404)
    return jsonify([obj.to_dict() for obj in city_obj.places])


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ Retrieves a place by its id """
    place_obj = storage.get("Place", place_id)
    if not place_obj:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """ Deletes a place """
    place_obj = storage.get("Place", place_id)
    if not place_obj:
        abort(404)
    storage.delete(place_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ Creates a Place """
    city_obj = storage.get("City", city_id)
    if not city_obj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if not storage.get("User", data["user_id"]):
        abort(404)
    if "name" not in data:
        abort(400, "Missing name")
    place_obj = Place(**data)
    place_obj.city_id = city_id
    place_obj.save()
    return make_response(jsonify(place_obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """ Updates a Place object"""
    place_obj = storage.get("Place", place_id)
    if not place_obj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_obj, key, value)
    place_obj.save()
    return make_response(jsonify(place_obj.to_dict()), 200)

#!/usr/bin/python3
""" module that handles all default RestFul API actions
"""

from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/places", strict_slashes=False, methods=['GET'])
def get_places():
    objs = storage.all('Place')
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False,
                 methods=['GET'])
def get_places_by_city(city_id):
    """ get all place objects given a state"""
    obj = storage.get("City", city_id)
    if not obj:
        abort(404)
    place_objs = obj.places
    return jsonify([place.to_dict() for place in place_objs])


@app_views.route("/places/<place_id>", strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """ get state object """
    obj = storage.get("Place", place_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/places/<place_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """delete state object"""
    obj = storage.get("Place", place_id)
    if obj:
        obj.delete()
        return jsonify({}), 200
    abort(404)


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False,
                 methods=['POST'])
def post_place(city_id):
    """create city instance"""
    request_dict = request.get_json()
    if not request_dict:
        abort(400, {"message": "Not a JSON"})
    if "user_id" not in request_dict:
        abort(400, {"message": "Missing user_id"})
    if not storage.get("User", request_dict['user_id']):
        abort(400)
    if "name" not in request_dict:
        abort(400, {"message": "Missing name"})
    obj = Place(**request_dict)
    obj.city_id = city_id
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False, methods=['PUT'])
def put_place(place_id):
    """update city object"""
    obj = storage.get("Place", place_id)
    if not obj:
        abort(404)
    request_dict = request.get_json()
    if not request_dict:
        abort(400, {"message": "Not a JSON"})
    for key, value in request_dict.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200

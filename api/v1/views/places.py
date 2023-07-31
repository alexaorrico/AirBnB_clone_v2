#!/usr/bin/python3
"""
view for Place objects that handles all default RestFul API actions

Potentially add 3 optional keys for 16(Advanced):
states: list of State ids
cities: list of City ids
amenities: list of Amenity ids
"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_places(city_id):
    """Retrieves the list of all Place objects or create a new Place object"""
    city_obj = storage.get("City", city_id)
    if city_obj:
        if request.method == 'GET':
            return jsonify([place_obj.
                            to_dict() for place_obj in city_obj.places]), 200
        if request.method == 'POST':
            if not request.get_json(silent=True):
                abort(400, "Not a JSON")
            if not request.get_json(silent=True).get('user_id'):
                abort(400, "Missing user_id")
            user_obj = storage.get("User", request.get_json(silent=True).
                                   get('user_id'))
            if not user_obj:
                abort(404)
            if not request.get_json(silent=True).get('name'):
                abort(400, "Missing name")
            kwargs = request.get_json(silent=True)
            new_place = Place(**kwargs)
            setattr(new_place, 'city_id', city_id)
            new_place.save()
            return jsonify(new_place.to_dict()), 201
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_byid(place_id):
    """Retrieves a Place object by id, delete or update a Place object"""
    place_obj = storage.get("Place", place_id)
    if place_obj:
        if request.method == 'GET':
            return jsonify(place_obj.to_dict()), 200
        elif request.method == 'DELETE':
            storage.delete(place_obj)
            storage.save()
            return {}, 200
        elif request.method == 'PUT':
            if not request.get_json(silent=True):
                abort(400, "Not a JSON")
            kwargs = request.get_json(silent=True)
            if kwargs:
                for key, value in kwargs.items():
                    if key not in ["id", "user_id", "city_id", "created_at",
                                   "updated_at"]:
                        setattr(place_obj, key, value)
                place_obj.save()
            return jsonify(place_obj.to_dict()), 200
    else:
        abort(404)

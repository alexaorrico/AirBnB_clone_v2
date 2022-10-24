#!/usr/bin/python3
"""Routings for amenity-related API requests"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<string:id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(id):
    """ get all instance of Place """
    if request.method == 'GET':
        city = storage.get(City, id)
        if city is None:
            abort(404)
        places = storage.all(Place)
        values = []
        for value in places:
            if value["city_id"] == id:
                values.append(value)
        return jsonify(values)


@app_views.route('/places/<string:id>', methods=['GET'],
                 strict_slashes=False)
def get_single_place(id):
    """"get an instance of Place """
    place = storage.get(Place, id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('places/<string:id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(id):
    """ delete an instance of Place """
    if request.method == 'DELETE':
        place = storage.get(Place, id)
        if place is None:
            abort(404)
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/cities/<string:id>/places', methods=['POST'],
                 strict_slashes=False)
def add_place(id):
    """ create an instance of Place """
    if request.method == 'POST':
        city = storage.get(City, id)
        if city is None:
            abort(404)
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        body = request.get_json()
        if "user_id" not in body:
            return make_response(jsonify({"error": "Missing user_id"}), 400)
        if "name" not in body:
            return make_response(jsonify({"error": "Missing name"}), 400)
        body.update({"city_id": id})
        new_place = Place(**body)
        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<string:id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(id):
    """ update an instance of Place """
    if request.method == 'PUT':
        place = storage.get(Place, id)
        if place is None:
            abort(404)
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        body = request.get_json()
        keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in body.items():
            if key not in keys:
                setattr(place, key, value)
        place.save()
        return make_response(jsonify(place.to_dict()), 200)

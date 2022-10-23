#!/usr/bin/python3
""" Places view """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def all_places(city_id):
    """ Returns a list of all the places """
    if not storage.get("City", city_id):
        abort(404)

    places = []
    for place in storage.all("Place").values():
        if place.city_id == city_id:
            places.append(place.to_dict())

    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place(place_id):
    """ Returns a place specified by id """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ Deletes a place specified by i d"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def add_place(city_id):
    """ Creates a new place based on city id """
    if not storage.get("City", city_id):
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    user_id = request.get_json().get('user_id')
    if not user_id:
        abort(400, description="Missing user_id")

    if not storage.get("User", user_id):
        abort(404)

    if not request.get_json().get('name'):
        abort(400, description="Missing name")

    place = Place()
    place.name = request.get_json()['name']
    place.city_id = city_id
    place.user_id = user_id
    place.save()

    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a place specified by id """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for key, value in request.get_json().items():
        if key == "id" or key == "created_at" \
           or key == "updated_at" or key == "user_id" or key == "city_id":
            continue
        else:
            setattr(place, key, value)
            
    storage.save()

    return make_response(jsonify(place.to_dict()), 200)

#!/usr/bin/python3
"""User views"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def places_get(city_id):
    """Retrieves the list of all PLace objects of a City"""
    if storage.get('City', city_id) is None:
        abort(404)
    all_places = storage.get('City', city_id).places
    places_for_json = []
    for place in all_places:
        places_for_json.append(place.to_dict())
    return jsonify(places_for_json)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_places(place_id):
    """Retrieves a Place object"""
    if storage.get('Place', place_id) is None:
        abort(404)
    return jsonify(storage.get('Place', place_id).to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    if not storage.get('Place', place_id):
        abort(404)
    else:
        storage.delete(storage.get('Place', place_id))
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_places(city_id):
    """Creates a PLace"""
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if "user_id" not in req:
        abort(400, "Missing user_id")
    if "name" not in req:
        abort(400, "Missing name")
    if storage.get('City', city_id) is None:
        abort(404)
    if storage.get('User', request.json['user_id']):
        abort(404)
    new_place = Place(name=request.json["name"],
                 city_id=city_id, user_id=request.json['user_id'])
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_places(place_id):
    """Updates a PLace object"""
    req = request.get_json()
    if storage.get('Place', place_id) is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    place_to_modify = storage.get('User', user_id)
    for key in req:
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_to_modify, key, req[key])
    storage.save()
    return jsonify(place_to_modify.to_dict()), 200

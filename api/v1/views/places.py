#!/usr/bin/python3
"""Flask app to handle Place API"""
from models import storage
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    places_list = [place.to_dict() for place in city_obj.places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place_by_id(place_id):
    """Retrieves a Place object"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    place_dict = place_obj.to_dict()
    return jsonify(place_dict)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place_by_id(place_id):
    """Deletes a Place object: DELETE"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    place_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place(city_id):
    """Retrieves the list of all Place objects of a City"""
    if storage.get("City", city_id) is None:
        abort(404)
    json_obj = request.get_json()
    if not request.json:
        return jsonify("Not a JSON"), 400
    if 'user_id' not in json_obj:
        return jsonify("Missing user_id"), 400
    user_id = json_obj['user_id']
    if storage.get("User", user_id) is None:
        abort(404)
    if 'name' not in json_obj:
        return jsonify("Missing name"), 400
    json_obj['city_id'] = city_id
    new_place_obj = Place(**json_obj)
    new_place_obj.save()
    new_place = new_place_obj.to_dict()
    return jsonify(new_place), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place_by_id(place_id):
    """Updates a Place object"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    json_obj = request.get_json()
    if not request.json:
        return jsonify("Not a JSON"), 400
    ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in json_obj.items():
        if key not in ignore:
            setattr(place_obj, key, value)
    place_obj.save()
    updated_place = place_obj.to_dict()
    return jsonify(updated_place), 200

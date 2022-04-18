#!/usr/bin/python3
"""
Place Module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, Place, City, User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_place(city_id):
    """ Retrieves the list of all Place objects of a City """
    places_obj = []
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404)
    for key, value in storage.all("Place").items():
        if value.city_id == city_id:
            places_obj.append(value.to_dict())
    return jsonify(places_obj)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def indv_place(place_id):
    """ Retrieves a Place object """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """ Deletes a Place object """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    place_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a Place """
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    req = request.json
    if not req:
        return jsonify({"error": "Not a JSON"}), 400
    p_req = request.get_json()
    if "user_id" not in p_req:
        return jsonify({"error": "Missing user_id"}), 400
    user_obj = storage.get("User", p_req["user_id"])
    if user_obj is None:
        abort(404)
    if "name" not in p_req:
        return jsonify({"error": "Missing name"}), 400
    else:
        new_user_id = p_req["user_id"]
        new_name = p_req["name"]
        new_place = Place(user_id=new_user_id, name=new_name, city_id=city_id)
        for key, value in p_req.items():
            setattr(new_place, key, value)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    req = request.get_json()
    place_obj = storage.get("Place", place_id)
    if not req:
        return (jsonify({'error': "Not a JSON"}), 400)
    if place_obj is None:
        abort(404)
    for key, val in req.items():
        if key not in ['id', 'created_at', 'user_id', 'city_id']:
            setattr(place_obj, key, val)
    place_obj.save()
    return (jsonify(place_obj.to_dict()), 200)

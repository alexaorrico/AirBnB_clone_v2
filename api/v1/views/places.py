#!/usr/bin/python3
"""Views for the Place class: GET, DELETE,  POST, PUT"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places_in_city(city_id):
    """Route that shows all instances of class Place in a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    objs = []
    for x in city.places:
        objs.append(x.to_dict())
    return jsonify(objs)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Route that shows a specific Place requested by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Route that shows after deleting Place instance with input id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Route that shows a new instance of Place after being created"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    user = storage.get(User, request.get_json()["user_id"])
    if not user:
        abort(404)

    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    d = request.get_json()
    d.update({"city_id": city_id})
    d.update({"user_id": d["user_id"]})
    obj = Place(**request.get_json())
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Route that shows instance of Place with input id after being updated"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    place.__dict__.update(request.get_json())
    old_dict = place.to_dict()
    storage.delete(place)
    place = Place(**old_dict)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 200

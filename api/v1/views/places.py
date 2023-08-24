#!/usr/bin/python3
"""places views"""
from models.city import City
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def retrives_all_places(city_id):
    """Retrives the list of all places"""
    if storage.get(City, city_id) is None:
        abort(404)
    city = storage.get(City, city_id)
    return jsonify([
        places.to_dict() for places in city.places])

@app_views.route('/places/<place_id>', methods=['GET'])
def retrives_place(place_id):
    """Retrives a Place from id"""
    if storage.get(Place, place_id) is None:
        abort(404)
    return jsonify(storage.get(Place, place_id).to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """creates a new place"""
    if storage.get(City, city_id) is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    if 'name' not in json_data:
        abort(400, 'Missing name')
    if 'user_id' not in json_data:
        abort(400, 'Missing user_id')
    place = Place(**json_data)
    setattr(place, 'city_id', city_id)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """update a place"""
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for key, values in json_data.items():
        if key not in ('id', 'created_at', 'updated_at', 'city_id', 'user_id'):
            setattr(place, key, values)
    place.save()
    return jsonify(place.to_dict()), 200

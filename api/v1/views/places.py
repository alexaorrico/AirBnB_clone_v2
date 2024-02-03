#!/usr/bin/python3
"""places view"""
from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def places_of_city(city_id):
    """display all places of a city"""
    city = storage.get(City, city_id)
    if city:
        return jsonify([place.to_dict() for place in city.places])

    abort(404)


@app_views.route('/places/<id>', methods=['GET'])
def place_by_id(id):
    """display place by id"""
    place = storage.get(Place, id)
    if place:
        return place.to_dict()
    abort(404)


@app_views.route('/places/<id>', methods=['DELETE'])
def delete_place(id):
    """delete a place by its id"""
    place = storage.get(Place, id)
    if place:
        storage.delete(place)
        storage.save()
        return {}
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """create a new place"""
    if not storage.get(City, city_id):
        abort(404)
    if not storage.get(User, data.get('user_id')):
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if not data.get('name'):
        abort(400, 'Missing name')
    if not data.get('user_id'):
        abort(400, 'Missing user_id')
    new_place = Place(city_id=city_id, **data)
    new_place.save()
    return new_place.to_dict(), 201


@app_views.route('places/<id>', methods=['PUT'])
def update_place(id):
    """update a place by its id"""
    place = storage.get(Place, id)
    if not place:
        return abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for k, v in data.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, v)
    storage.save()
    return place.to_dict()

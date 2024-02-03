#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from flask import abort, jsonify, request
import json


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def all_places(city_id):
    place_list = []
    place_dict = storage.all(Place)
    for place in place_dict.values():
        if city_id == place.city_id:
            place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def places_id(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['DELETE'])
def places_delete(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify('{}'), 201


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def places_post(city_id):
    try:
        data = request.get_data()
        data_object = json.loads(data.decode('utf-8'))
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        data_object['city_id'] = city_id
        if 'user_id' not in data_object:
            abort(400, 'Missing user_id')
        if 'name' not in data_object:
            abort(400, 'Missing name')
        user = storage.get(User, data_object['user_id'])
        if not user:
            abort(404)
        new_place = Place(**data_object)
        storage.new(new_place)
        storage.save()
    except json.JSONDecodeError:
        abort(400, 'Not a JSON')
    return jsonify(new_place.to_dict()), 201


@app_views.route('places/<place_id>', methods=['PUT'])
def places_put(place_id):
    try:
        place_up = storage.get(Place, place_id)
        if not place_up:
            abort(404)
        data = request.get_data()
        data_object = json.loads(data.decode('utf-8'))
        for key, value in data_object.items():
            setattr(place_up, key, value)
        storage.save()
    except json.JSONDecodeError:
        abort(400, 'Not a JSON')
    return jsonify(place_up.to_dict()), 201

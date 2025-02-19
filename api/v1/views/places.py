#!/usr/bin/python3
"""Places management"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from datetime import datetime
import uuid


@app_views.route('/cities/<city_id>/places', methods=['GET'])
@app_views.route('/cities/<city_id>/places/', methods=['GET'])
def list_places_of_city(city_id):
    '''Fetches all Place objects within a specified city'''
    cities_data = storage.all("City").values()
    city_data = [item.to_dict() for item in cities_data if item.id == city_id]
    if not city_data:
        abort(404)
    places_data = [item.to_dict() for item in storage.all("Place").values()
                   if city_id == item.city_id]
    return jsonify(places_data)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    '''Fetches a specific Place object by ID'''
    places_data = storage.all("Place").values()
    place_data = [item.to_dict() for item in places_data if item.id == place_id]
    if not place_data:
        abort(404)
    return jsonify(place_data[0])


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''Deletes a specific Place object by ID'''
    places_data = storage.all("Place").values()
    place_data = [item.to_dict() for item in places_data
                  if item.id == place_id]
    if not place_data:
        abort(404)
    place_data.remove(place_data[0])
    for item in places_data:
        if item.id == place_id:
            storage.delete(item)
            storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    '''Creates a new Place within a specified city'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    cities_data = storage.all("City").values()
    city_data = [item.to_dict() for item in cities_data
                 if item.id == city_id]
    if not city_data:
        abort(404)
    places_list = []
    new_place = Place(name=request.json['name'],
                      user_id=request.json['user_id'], city_id=city_id)
    users_data = storage.all("User").values()
    user_data = [item.to_dict() for item in users_data
                 if item.id == new_place.user_id]
    if not user_data:
        abort(404)
    storage.new(new_place)
    storage.save()
    places_list.append(new_place.to_dict())
    return jsonify(places_list[0]), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    '''Updates a specific Place object'''
    places_data = storage.all("Place").values()
    place_data = [item.to_dict() for item in places_data if item.id == place_id]
    if not place_data:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' in request.get_json():
        place_data[0]['name'] = request.json['name']
    if 'description' in request.get_json():
        place_data[0]['description'] = request.json['description']
    if 'number_rooms' in request.get_json():
        place_data[0]['number_rooms'] = request.json['number_rooms']
    if 'number_bathrooms' in request.get_json():
        place_data[0]['number_bathrooms'] = request.json['number_bathrooms']
    if 'max_guest' in request.get_json():
        place_data[0]['max_guest'] = request.json['max_guest']
    if 'price_by_night' in request.get_json():
        place_data[0]['price_by_night'] = request.json['price_by_night']
    if 'latitude' in request.get_json():
        place_data[0]['latitude'] = request.json['latitude']
    if 'longitude' in request.get_json():
        place_data[0]['longitude'] = request.json['longitude']
    for item in places_data:
        if item.id == place_id:
            if 'name' in request.get_json():
                item.name = request.json['name']
            if 'description' in request.get_json():
                item.description = request.json['description']
            if 'number_rooms' in request.get_json():
                item.number_rooms = request.json['number_rooms']
            if 'number_bathrooms' in request.get_json():
                item.number_bathrooms = request.json['number_bathrooms']
            if 'max_guest' in request.get_json():
                item.max_guest = request.json['max_guest']
            if 'price_by_night' in request.get_json():
                item.price_by_night = request.json['price_by_night']
            if 'latitude' in request.get_json():
                item.latitude = request.json['latitude']
            if 'longitude' in request.get_json():
                item.longitude = request.json['longitude']
    storage.save()
    return jsonify(place_data[0]), 200

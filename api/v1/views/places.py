#!/usr/bin/python3
"""
New view for Place objects that handles all default RESTFul API actions
"""

from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage, City, Place, User

# Route to retrieve a list of all Place objects of a City
@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    """get a list of all place objects of a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

# Route to retrieve a specific Place object by place_id
@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """get a specific place object by place id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

# Route to delete a specific Place object by place_id
@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """delete a specific place object by place id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

# Route to create a new Place object
@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """create a new place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'name' not in data:
        abort(400, description="Missing name")
    
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    
    new_place = Place(**data)
    new_place.city_id = city_id
    new_place.save()
    
    return jsonify(new_place.to_dict()), 201

# Route to update a specific Place object by place_id
@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """update a specific place object by place id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    
    # Ignore keys: id, user_id, city_id, created_at, updated_at
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    
    place.save()
    
    return jsonify(place.to_dict()), 200

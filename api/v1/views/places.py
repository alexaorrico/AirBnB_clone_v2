#!/usr/bin/python3
"""
Module Places
"""
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    
    places = city.places
    places_list = [place.to_dict() for place in places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """
    Retrieves a Place object by ID
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object by ID
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
    Creates a new Place
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    
    content = request.get_json()
    if content is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in content:
        return jsonify({'error': 'Missing user_id'}), 400
    
    user = storage.get(User, content['user_id'])
    if user is None:
        abort(404)
    
    if 'name' not in content:
        return jsonify({'error': 'Missing name'}), 400
    
    content['city_id'] = city_id
    new_place = Place(**content)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object by ID
    """
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    
    content = request.get_json()
    if content is None:
        return jsonify({'error': 'Not a JSON'}), 400
    
    for key, value in content.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    
    place.save()
    return jsonify(place.to_dict()), 200
#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Places """
from models.state import State
from models.city import City
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    list all places by city id
    """
    city = storage.get(City, city_id)
    all_places = storage.all(Place).values()

    if not city:
        abort(404)

    for place in all_places:
        if place.city_id == city_id:
            places.append(place)

    return jsonify(places)

@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """
    get a place by id
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    return jsonify(place)

@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    delete a place by id
    """
    place = storage.get(Place, place_id)
    
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    create a place
    """
    city = storage.get(City, city_id)
    
    if not city:
        abort(404)
    
    new_data = request.get_json()
    if not new_data:
        abort(400, description="Not a JSON")

    if 'user_id' not in new_data:
        abort(400, description="Missing user_id")

    if 'name' not in new_data:
        abort(400, description="Missing name")

    new_place = Place(**new_data)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    update a place
    """
    place = storage.get(Place, place_id)
    
    if not place:
        abort(404)

    new_data = request.get_json()
    if not new_data:
        abort(400, description="Not a JSON")

    for key, value in new_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200

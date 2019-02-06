#!/usr/bin/python3
"""
module that defines API interactions for Places __objects
"""
from models import storage
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_places(city_id):
    """
    defines the places route
    Returns: list of all Place objects associated with a City obj
    """
    city = storage.get("City", city_id)

    if not city:
        abort(404)

    return jsonify([place.to_dict() for place in city.places]), 200


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=["GET"])
def id_for_place(place_id):
    """
    defines the places/<place_id> route
    Returns: place id or 404 Error if object not linked to Place object
    """
    a_place = storage.get("Place", place_id)
    if a_place:
        return jsonify(a_place.to_dict()), 200
    return abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place_id(place_id):
    """
    defines Delete for Place objects by id
    Returns: if successful 200 and an empty dictionary
             404 if place_id is not linked to any Place obj
    """
    place = storage.get("Place", place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/cities/<city_id>/places/',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """
    define how to create a new place object
    Returns: 201 on successful creation
             400 "Not a JSON" if HTTP body request is not valid
    """
    places = request.get_json()

    if places is None:
        return abort(400, 'Not a JSON')
    if places.get("name") is None:
        return abort(400, 'Missing name')
    if places.get("user_id") is None:
        return abort(400, 'Missing user_id')

    city = storage.get("City", city_id)
    if not city:
        abort(404)

    user = storage.get("User", places['user_id'])
    if not user:
        abort(404)

    new_place = Place(**places)

    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['PUT'])
def place_update(place_id):
    """
    defines how an Update to a place is made
    Returns: 200 and the place object if successful
             400 "Not a JSON" if HTTP body request is not valid
             404 if state_id is not linked to any Place object
    """
    place_data = request.get_json()

    if not place_data:
        return abort(400, 'Not a JSON')

    place = storage.get('Place', place_id)

    if not place:
        return abort(404)

    for key, value in place_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()

    return jsonify(place.to_dict()), 200

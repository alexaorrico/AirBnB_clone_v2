#!/usr/bin/python3
"""ALX SE Flask Api Place Module."""
from api.v1.app import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id: str):
    """Return list of all places link to the current city."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id: str):
    """Return a place given its id."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_place(place_id: str):
    """Delete a place given its id from storage."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route(
        '/cities/<city_id>/places',
        methods=['POST'],
        strict_slashes=False)
def create_place(city_id: str):
    """Create a new place in storage."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        place_attrs = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if 'name' not in place_attrs:
        abort(400, 'Missing name')
    place = Place(**place_attrs)
    place.city_id = city_id
    storage.new(place)
    storage.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id: str):
    """Update a place given its id."""
    try:
        place_attrs = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for attr, value in place_attrs.items():
        if attr not in ('id', 'city_id', 'updated_at', 'created_at'):
            setattr(place, attr, value)
    place.save()
    return jsonify(place.to_dict())

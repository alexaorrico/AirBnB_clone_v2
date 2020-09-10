#!/usr/bin/python3
"""Places Api Module"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places_id(city_id):
    """Return all Places objects through the HTTP GET request."""
    if storage.get(City, city_id) is None:
        abort(404)
    all_places = storage.all(Place).values()
    specific_places = []
    for place in all_places:
        if place.city_id == city_id:
            specific_places.append(place.to_dict())
    return jsonify(specific_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def places_id_get(place_id):
    """Get a specific Place object through the HTTP GET request."""
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    return jsonify(obj_place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def places_id_delete(place_id):
    """Delete a specific Place object through the HTTP DELETE request."""
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    storage.delete(obj_place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def places_push(city_id):
    """Create a new Place object through the HTTP POST request"""
    if storage.get(City, city_id) is None:
        abort(404)
    if not request.get_json(silent=True):
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    if "user_id" not in req:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if storage.get(User, req['user_id']) is None:
        abort(404)
    if "name" not in req:
        return make_response(jsonify({"error": "Missing name"}), 400)
    req['city_id'] = city_id
    place = Place(**req)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def places_id_put(place_id):
    """Update a specific Place object through the HTTP PUT request."""
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    if not request.get_json(silent=True):
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    for key, value in req.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(obj_place, key, value)
    obj_place.save()
    return make_response(jsonify(obj_place.to_dict()), 200)

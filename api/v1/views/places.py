#!/usr/bin/python3
"""
API endpoints related to Place objects
"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """
    Retrieves all Place objects associated with a City
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object based on its ID
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object based on its ID
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
    Creates a new Place object associated with a City
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    if 'user_id' not in req:
        abort(400, 'Missing user_id')
    if 'name' not in req:
        abort(400, 'Missing name')
    user = storage.get(User, req['user_id'])
    if user is None:
        abort(404)
    req['city_id'] = city_id
    place = Place(**req)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object based on its ID
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    for key, value in req.items():
        if key not in ['id', 'created_at', 'updated_at', 'city_id', 'user_id']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

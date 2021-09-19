#!/usr/bin/python3
""" Routes for State responses """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, city, place
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=["GET"],
                 strict_slashes=False)
def all_places(city_id=None):
    """retrieves a list of all places in a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    places_list = [place.to_dict() for place in places]
    return (jsonify(places_list), 200)


@app_views.route('/places/<place_id>', methods=["GET"], strict_slashes=False)
def specific_place(place_id=None):
    """Get place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return (jsonify(place.to_dict()), 200)


@app_views.route('/places/<place_id>', methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """ Deletes a place by ID """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates new place in a city """
    req = request.get_json()
    if req is False:
        abort(400, "Not a JSON")
    if "name" not in req:
        abort(400, "Missing name")
    if storage.get(City, city_id) is None:
        abort(404, "city id not found")
    if "user_id" not in req:
        abort(400, "Missing user_id")
    user = storage.get(User, req.get('user_id'))
    if not user:
        abort(404)
    
    new_place = Place()
    new_place.city_id = city_id
    for key, value in req.items():
        setattr(new_place, key, value)
    new_place.save()
    return (jsonify(new_place.to_dict()), 201)

@app_views.route('/places/<place_id>', methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """ Update a place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(place, key, value)
    place.save()
    return (jsonify(place.to_dict()), 200)

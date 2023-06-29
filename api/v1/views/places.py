#!/usr/bin/python3
'''Contains the places view for the API.'''
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def places(place_id):
    """Retrieves a place object"""
    places_obj = storage.get(Place, place_id)
    if places_obj is None:
        abort(404)
    else:
        return jsonify(places_obj.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def city_places(city_id):
    """Retrieves the list of all place objects of a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify([places.to_dict() for places in city.places])


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_places(place_id):
    """Deletes a places object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>places', methods=['POST'],
                 strict_slashes=False)
def post_places(city_id):
    """Creates a places"""
    obj_city = storage.get(City, city_id)
    if not obj_city:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, "Missing user_id")
    user_id = request.get_json()['user_id']
    obj_user = storage.get(User, user_id)
    if not obj_user:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    obj = Place(**request.get_json(), city_id=city_id)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_places(place_id):
    """Updates a places object"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(obj, k, v)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)

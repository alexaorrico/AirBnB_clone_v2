#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for Places """
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route(
        '/cities/<city_id>/places',
        methods=['GET'],
        strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all place objects
    or a specific city
    """
    all_places = storage.all(Place).values()
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    list_specific_places = []
    for place in all_places:
        if place.city_id == city_id:
            list_specific_places.append(place.to_dict())
    return jsonify(list_specific_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a place by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a place Object
    """

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
        '/cities/<city_id>/places',
        methods=['POST'],
        strict_slashes=False)
def post_place(city_id):
    """
    Creates a place
    """
    city = storage.get(City, city_id)

    user_id = request.get_json().get("user_id")
    user = storage.get(User, user_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if not user:
        abort(404)

    data = request.get_json()
    instance = Place(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """
    Updates a place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)

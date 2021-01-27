#!/usr/bin/python3
"""new view for Place objects that handles all
default RestFul API actions
"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route(
    "/cities/<city_id>/places", methods=['GET'], strict_slashes=False)
def places_view(city_id):
    """Retrieves the list of all Place objects of a City"""
    my_city = storage.get(City, city_id)
    if my_city is None:
        abort(404)

    for place in storage.all(Place).values():
        list_places = []
        if place.city_id == city_id:
            list_places.append(place.to_dict())
        return jsonify(list_places)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def place_view(place_id):
    """Retrieves a Place object"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    return jsonify(my_place.to_dict())


@app_views.route(
    "/places/<place_id>", methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    storage.delete(my_place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/cities/<city_id>/places", methods=['POST'], strict_slashes=False)
def post_place(place_id):
    """Create a new Place object"""
    my_city = storage.get(City, city_id)
    if my_city is None:
        abort(404)

    content = request.get_json(my_city)
    if content is None:
        abort(400, "Not a JSON")

    user_id = content.get('user_id')
    if user_id is None:
        abort(400, "Missing user_id")

    if storage.get(User, user_id) is None:
        abort(404)

    if content.get('name') is None:
        abort(400, "Missing name")

    new_place = Place(**content)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates a Place object"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    content = request.get_json(my_place)
    if content is None:
        abort(400, "Not a JSON")

    keys_ignored = ['id', 'user_id', 'city_id' 'created_at', 'updated_at']
    for key, value in content.items():
        if key not in keys_ignored:
            setattr(st, key, value)
    st.save()
    return jsonify(st.to_dict()), 200

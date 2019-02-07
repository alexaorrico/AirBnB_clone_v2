#!/usr/bin/python3
""" Place RESTful API """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """ Uses to_dict to retrieve an object into a valid JSON """
    all_cities = storage.all("City")
    if all_cities is None:
        abort(404)
    all_places = storage.all("Place")
    list = []
    for place in all_places.values():
        if place.city_id == city_id:
            list.append(place.to_dict())
    return jsonify(list)

@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def individual_places(place_id):
    """ Retrieves a Place object, or returns a 404 if the place_id is not
    linked to any object """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object, or returns a 404 if the place_id is not
    linked to any object """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ Creates a Place object, or returns a 400 if the HTTP body request
    is not valid JSON, or if the dict doesnt contain the key name """
    city = storage.get("City", city_id)
    city_list = [city.id for city in storage.all("City").values()]
    if city is None or city not in city_list:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    user_id = data.get('user_id')
    if user_id is None:
        abort(400, "Missing user_id")
    user_list = [user.id for user in storage.all("User").values()]
    if user_id not in user_list:
        abort(404)
    name = data.get("name")
    if name is None:
        abort(400, "Missing name")

    new_user_id = user_id
    new_place = Place()
    new_place.user_id = new_user_id
    new_place.name = name
    new_place.city_id = city_id
    for key, value in data.items():
        setattr(new_place, key, value)
    new_place.save()
    return (jsonify(new_place.to_dict())), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates an Place object, or returns a 400 if the HTTP body is not valid
    JSON, or a 404 if state_id is not linked to an object """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = ""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for k, v in data.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, v)
    place.save()
    return (jsonify(place.to_dict()))

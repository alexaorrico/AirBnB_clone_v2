#!/usr/bin/python3
"""
Creating a new view for Place objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('cities/<city_id>/places', strict_slashes=False,
                 methods=['Get'])
def list_of_places_for_city(city_id):
    """retrieves list of places based on id"""
    city = storage.get("City", city_id)
    places = []
    if city is None:
        abort(404)
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_on_id(place_id):
    """ get place by based on place id given """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_id(place_id):
    """ deletes a place based on its id """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def add_place(city_id):
    """ adding a new place for given city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in json_data:
        abort(400, description='Missing user_id')
    if 'name' not in json_data:
        abort(400, description="Missing name")
    user_id = json_data['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    json_data['city_id'] = city_id
    place = Place(**json_data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def updating_place(place_id=None):
    """updates place based on given id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        abort(404, description="Not a JSON")
    for k, v in json_data.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200

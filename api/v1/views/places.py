#!/usr/bin/python3
""" Handle RESTful API request for states"""

from models.state import State
from models.place import Place
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """ GET ALL PLACES """
    city = storage.all(City).values()
    if not city:
        abort(404)
    places_list = city.places
    places_dict = []
    for place in places_list:
        places_dict.append(place.to_dict())

    return jsonify(places_dict)

@app_views.route('/places/<place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_places(place_id):
    """ Retrieves a specific user """
    instance = storage.get(Place, place_id)
    if not instance:
        abort(404)
    return jsonify(instance.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    obj = storage.get(Place, place_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a amenity """

    if not request.get_json():
        abort(400, description="Not a JSON")
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    data['city_id'] = city_id

    if not 'name' in data:
        abort(400, description="Missing name")
    if not 'user_id' in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    new_instance = Place(**data)
    new_instance.save()

    return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """update a State: POST /api/v1/states"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    obj = storage.get(Place, place_id)

    if not obj:
        abort(404)

    data = request.get_json()

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(obj, key, value)
    storage.save()

    return make_response(jsonify(obj.to_dict()), 200)

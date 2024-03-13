#!/usr/bin/python3
""" Amenity module """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.city import City
from models.place import Place
from models import storage
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    """ Retrieves a list of all Place objects linked to a City """
    places = []
    city_obj = storage.get(City, city_id)
    if city_obj:
        for obj in storage.all(Place).values():
            if obj.city_id == city_id:
                places.append(obj.to_dict())
        return make_response(jsonify(places), 200)
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def one_place(place_id):
    """ Retrieves one object using its id """
    obj = storage.get(Place, place_id)
    if obj:
        return make_response(jsonify(obj.to_dict()), 200)
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """ Deletes a Place obj """
    obj = storage.get(Place, place_id)
    if obj:
        obj.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a new Place object """
    if request.is_json is True:
        data = request.get_json()
        if storage.get(City, city_id):
            if 'user_id' not in data.keys():
                abort(400, "Missing user_id")
            if 'name' not in data.keys():
                abort(400, "Missing name")
            if storage.get(User, data['user_id']):
                data["city_id"] = city_id
                obj = Place(**data)
                storage.new(obj)
                storage.save()
                return make_response(jsonify(obj.to_dict()), 201)
            abort(404)
        abort(404)
    abort(400, "Not a JSON")


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ Updates an existing Place object """
    if request.is_json is True:
        data = request.get_json()
        obj = storage.get(Place, place_id)
        if obj:
            for key, value in data.items():
                if key not in ['id', 'user', 'city_id', 'created_at',
                               'updated_at']:
                    setattr(obj, key, value)
            obj.save()
            return make_response(jsonify(obj.to_dict()), 200)
        abort(404)
    abort(400, "Not a JSON")

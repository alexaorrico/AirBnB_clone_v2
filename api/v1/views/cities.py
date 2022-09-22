#!/usr/bin/python3
""" create a new view for City objects that handles all default RESTFul API actions """
from api.v1.views import app_views
from flask import abort, jsonify, request
import models
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def all_cities(state_id):
    """ 
    Retrieves the list of all City objects of a State
    If the state_id is not linked to any State object, raise a 404 error
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    all_cities_dict = storage.all(City)
    cities_list = []
    for city in all_cities_dict.values():
        if state_id == city.state_id:
            cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_get(city_id):
    """ Retrieves a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def city_delete(city_id):
    """ Deletes a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def city_post(state_id):
    """ Adds a City to given state id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        content = request.json
        if 'name' not in content:
            abort(400, "Missing name")
        new_city = City(name=content['name'], state_id=state_id)
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    else:
        abort(400, "Not a JSON")


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_put(city_id):
    """ Update a city object based on given city id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
        
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        content = request.json
        new_dict = {}
        for k, v in content.items():
            if k not in ["id", "created_at", "updated_at"]:
                new_dict[k] = v
        city.update(**new_dict)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(400, "Not a JSON")

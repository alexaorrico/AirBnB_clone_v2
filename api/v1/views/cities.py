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
import json


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
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
    empty_dict = {}
    storage.delete(city)
    storage.save()
    return jsonify(empty_dict), 200

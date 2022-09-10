#!/usr/bin/python3
"""file cities"""
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort
import json

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cityobjs(state_id=None):
    """Function that retrieves all city obj of a State"""
    try:    
        list_of_cities = []
        state = storage.get("State", state_id)
        for city in state.cities:
            list_of_cities.append(city.to_dict())
        return jsonify(list_of_cities)
    except Exception as error:
        abort(404)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def citybjs(city_id=None):
    """Function that returns an obj if it matches city_id"""
    cities = storage.all(City)
    for key, value in cities.items():
        if cities[key].id == city_id:
            return value.to_dict()
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def deleteobj(city_id=None):
    """Function to delete an obj"""
    cities = storage.all(City)
    for key, value in cities.items():
        if cities[key].id == city_id:
            storage.delete(cities[key])
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def createcity(state_id=None):
    """Function to create an obj"""
    body = request.get_json()
    if body is None:
        return jsonify({
            "error": "Not a JSON"
        }), 400
    elif "name" not in body.keys():
        return jsonify({
            "error": "Missing Name"
        }), 400

    city = storage.get(City)
    if city is None:
        abort(404)
    else:
        new_city = City(**body)
        new_city.state_id = state_id
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updatecity(city_id=None):
    """Function to update a city obj"""
    try:
        notAttr = ['id', 'state_id', 'created_at', 'updated_at']
        body = request.get_json()
        cities = storage.all(City)
        for key, value in cities.items():
            if cities[key].id == city_id:
                for k, v in body.items():
                    if k not in notAttr:
                        setattr(value, k, v)
                value.save()
                return jsonify(value.to_dict()), 200
        abort(404)
    except Exception as err:
        return jsonify({
                    "error": "Not a JSON"
                }), 400
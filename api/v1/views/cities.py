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
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def deleteobj(city_id=None):
    """Function to delete an obj"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


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

    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    new_city = City(**body)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updatecity(city_id=None):
    """Function to update a city obj"""
    notAttr = ['id', 'state_id', 'created_at', 'updated_at']
    body = request.get_json()
    if body is None:
        return jsonify({
            "error": "Not a JSON"
        }), 400

    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    for key, value in body.items():
        if key not in notAttr:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200

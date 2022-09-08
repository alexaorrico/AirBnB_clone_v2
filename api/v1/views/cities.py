#!/usr/bin/python3
# City class
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

@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cityobjs(state_id=None):
    """Function that retrieves all city obj of a State"""
    list_of_cities = []
    if request.method == 'GET':
        if state_id is None:
            abort(404)
        else:
            cities = storage.all(City)
            for key, value in cities.items():
                if cities[key].state_id == state_id:
                    obj = value.to_dict()
                    list_of_cities.append(obj)
            if len(list_of_cities) == 0:
                abort(404)
            else:
                return jsonify(list_of_cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def citybjs(city_id=None):
    """Function that returns an obj if it matches city_id"""
    if request.method == 'GET':
        if city_id is None:
            abort(404)
        else:
            cities = storage.all(City)
            for key, value in cities.items():
                if cities[key].id == city_id:
                    return jsonify(value.to_dict())
            abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def deleteobj(city_id=None):
    """Function to delete an obj"""
    if request.method == 'DELETE':
        cities = storage.all(City)
        for key, value in cities.items():
            if cities[key].id == city_id:
                storage.delete(cities[key])
                storage.save()
                return jsonify({})
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def createcity(state_id=None):
    """Function to create an obj"""
    try:
        body = request.get_json()
        states = storage.all(State)
    except Exception as err:
        return jsonify({
                    "error": "Not a JSON"
                }), 400

# Continuar desde POST method


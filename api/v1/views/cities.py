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
    list_of_cities = []
    states = storage.all(State)
    for key, value in states.items():
        if value.id == state_id:
            for i in value.cities:
                list_of_cities.append(i.to_dict())
    if len(list_of_cities) == 0:
        return jsonify({'error': 'Not found'}), 404
    else:
        return jsonify(list_of_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
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


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
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


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def createcity(state_id=None):
    """Function to create an obj"""
    try:
        body = request.get_json()
        states = storage.all(State)
        for key, value in states.items():
            if value.id == state_id:
                if 'name' in body:
                    dic = {}
                    dic['name'] = body["name"]
                    dic['state_id'] = state_id
                    new_city = City(**dic)
                    new_city.save()
                    return jsonify(new_city.to_dict())
                else:
                    return jsonify({
                            "error": "Missing name"
                        }), 400
        return jsonify({'error': 'Not found'}), 404
    except Exception as err:
        return jsonify({
            "error": "Not a JSON"
        }), 400


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_cities_id(city_id):
    """
    Make a POST request HTTP to update data.
    """
    # Hacemos la request de la data que se pase en formato json y la
    # pasamos a un dic de python para poder trabajar con ella
    body = request.get_json()

    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Traemos todos los objetos de la clase State que esten en el storage
    city = storage.get(City, city_id)

    if city is None:
        # Se usa el metodo abort de flask en caso que no se pase una ID
        abort(404)
    else:
        # keys to ignore - not change
        keys_ignore = ["id", "state_id", "created_at", "updated_at"]

        for key, value in body.items():
            if key not in keys_ignore:
                setattr(city, key, value)
            else:
                pass
        # Se guarda el nuevo objeto dentro del storage
        storage.save()
        # Se devuelve el objeto creado y un status code de 200
        return make_response(jsonify(city.to_dict()), 200)
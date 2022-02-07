#!/usr/bin/python3
"""
module for city views
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """ Retrieves the list of all State's cities objects """
    states = storage.all("State")
    response = []
    for key in states.keys():
        if key.split('.')[-1] == state_id:
            list_cities = states.get(key).cities
            for city in list_cities:
                response.append(city.to_dict())
            return jsonify(response)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Retrieves a City object """
    cities = storage.all("City")
    for key in cities.keys():
        if key.split('.')[-1] == city_id:
            return jsonify(cities.get(key).to_dict())
    abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    cities = storage.all("City")
    for key in cities.keys():
        if key.split('.')[-1] == city_id:
            storage.delete(cities.get(key))
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ Creates a City """
    dic = request.get_json()
    if not dic:
        abort(400, "Not a JSON")
    if not ('name' in dic.keys()):
        abort(400, "Missing name")
    states = storage.all('State')
    for key in states.keys():
        if key.split('.')[-1] == state_id:
            city = City(state_id=state_id, **dic)
            city.save()
            return jsonify(city.to_dict()), 201
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ Updates a City object """
    cities = storage.all("City")
    city = None
    for key in cities.keys():
        if key.split('.')[-1] == city_id:
            city = cities.get(key)
    if not city:
        abort(404)
    new_dict = request.get_json()
    if not new_dict:
        abort(400, "Not a JSON")
    for key, value in new_dict.items():
        if key in ('id', 'created_at', 'updated_at'):
            continue
        else:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200

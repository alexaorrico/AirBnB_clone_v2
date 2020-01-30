#!/usr/bin/python3
"""
Cities file for APi project
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def list_cities(state_id):
    """lists all cities"""
    s_list = []
    states = storage.all("State")
    s_id = "State." + state_id
    if states.get(s_id) is None:
        abort(404)
    else:
        cities = storage.all("City")
        for city in cities.values():
            if city.state_id == state_id:
                s_list.append(city.to_dict())
    return jsonify(s_list)


@app_views.route('/cities/<city_id>>', methods=['GET'])
def GetCityById(city_id):
    """Retrieves city based on its id for GET HTTP method"""
    all_cities = storage.all("City")
    for city in all_cities.values():
        if city.id == city_id:
            return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def DeleteCityById(city_id):
    """Deletes a city based on its id for DELETE HTTP method"""
    cities = storage.all('City')
    c_id = "City." + city_id
    to_del = cities.get(c_id)
    if to_del is None:
        abort(404)
    storage.delete(to_del)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def PostCity(state_id):
    """Posts a city"""
    info = request.get_json()
    states = storage.all("State")
    pair = "State." + state_id
    if states.get(pair) is None:
        abort(404)
    if not info:
        abort(400, 'Not a JSON')
    elif "name" not in info:
        abort(400, 'Missing name')
    city = City()
    city.name = info['name']
    city.state_id = state_id
    city.save()
    city = city.to_dict()
    return jsonify(city), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def PutState(city_id):
    """ Updates a City uses PUT HTTP method"""
    exists = False
    all_cities = storage.all("City")
    for city in all_cities.values():
        if city.id == city_id:
            exists = True
    if not exists:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, 'Not a JSON')
    upt_city = all_cities['{}.{}'.format('City', city_id)]
    upt_city.name = info['name']
    upt_city.save()
    upt_city = upt_city.to_dict()
    return jsonify(upt_city), 201


if __name__ == '__main__':
    pass

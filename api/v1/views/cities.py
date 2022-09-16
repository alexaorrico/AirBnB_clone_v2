#!/usr/bin/python3
"""view cities object"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request

@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def cities_by_states(state_id):
    """return list of all object cities"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    cities = list()
    list_cities = storage.all('City')
    for value in list_cities.values():
        if state_id == value.state_id:
            cities.append(value.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def city_by_id(city_id):
    """Get cities by ID"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_cities(city_id):
    """Deletes an specific city"""
    ret = storage.get('City', city_id)
    if ret:
        storage.delete(ret)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_cities(state_id):
    """Create a new city"""
    from models.city import City
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    content = request.get_json(force=True, silent=True)
    if not content:
        abort(400, "Not a JSON")
    if "name" not in content.keys():
        abort(400, "Missing name")
    name_city = content.get('name')

    new_instance = City(name=name_city)
    return jsonify(new_instance.to_dict()), 201


@app_views.route('/cities/<cities_id>', strict_slashes=False, methods=['PUT'])
def update_city(cities_id):
    """Update a state by a given ID"""
    new_city = storage.get('City', cities_id)
    if not new_city:
        abort(404)

    content = request.get_json(force=True, silent=True)
    if not content:
        abort(400, "Not a JSON")

    to_ignore = ['id', 'created_at', 'update_at']
    for key, value in content.items():
        if key in to_ignore:
            continue
        else:
            setattr(new_city, key, value)
    storage.save()
    return jsonify(new_city.to_dict()), 200

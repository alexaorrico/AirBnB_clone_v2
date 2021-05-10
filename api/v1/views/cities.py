#!/usr/bin/python3
'''Creates routes that handles states with JSON'''
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'], strict_slashes=False)
def state_id_cities(state_id):
    '''returns list of states or creates new one'''
    state_target = storage.get(State, state_id)
    if state_target is None:
        abort(404)
    if request.method == 'POST':
        try:
            content = request.get_json()
            if content is None:
                abort(400, 'Not a JSON')
        except Exception as e:
            abort(400, 'Not a JSON')
        if 'name' not in content.keys():
            abort(400, 'Missing name')
        new_instance = City(state_id=state_id, name=content['name'])
        new_instance.save()
        return jsonify(new_instance.to_dict()), 201
    else:
        city_list = []
        for city_obj in state_target.cities:
            city_list.append(city_obj.to_dict())
        return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def cities_specific(city_id):
    '''manages specific state object'''
    city_target = storage.get(City, city_id)
    if city_target is None:
        abort(404)
    if request.method == 'PUT':
        try:
            content = request.get_json()
            if content is None:
                abort(400, 'Not a JSON')
        except Exception as e:
            abort(400, 'Not a JSON')
        ignore = ['id', 'state_id', 'created_at', 'updated_at']
        for key, val in content.items():
            if key not in ignore:
                setattr(city_target, key, val)
        city_target.save()
        return jsonify(city_target.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city_target)
        storage.save()
        return jsonify({})
    else:
        return jsonify(city_target.to_dict())

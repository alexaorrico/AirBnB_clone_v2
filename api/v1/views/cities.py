#!/usr/bin/python3
'''Module for City Rest API'''
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET', 'POST'])
def city_list(state_id):
    '''Interested in list of cities of particular states'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        list_city = [city.to_dict() for city in state.cities]
        return jsonify(list_city)
    if request.method == 'POST':
        try:
            json_body = request.get_json()
            if not json_body:
                abort(400, 'Not a JSON')
            if json_body['name'] is None:
                abort(400, 'Missing name')
            city = City(**json_body)
            city.state_id = state_id
            new_inst = storage.new(city)
            storage.save()
            return jsonify(city.to_dict()), 201
        except Exception as err:
            abort(404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def city_detail(city_id):
    '''Interested in details of a specific state'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({})
    else:
        try:
            json_body = request.get_json()
            if not json_body:
                abort(400, 'Not a JSON')
            for k, v in json_body.items():
                if k not in ['id', 'state_id', 'created_at', 'updated_at']:
                    setattr(city, k, v)
            storage.save()
            return jsonify(city.to_dict())
        except Exception as err:
            abort(404)

#!/usr/bin/python3
""" API """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, storage_t
from models.review import Review
from models.state import State
from models.city import City
from models.place import Place


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """ state """
    state = storage.get(State, state_id)
    if state:
        cities = list(map(lambda x: x.to_dict(), state.cities))
        return jsonify(cities)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """ city """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def add_city(state_id):
    """ New city """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, description='Missing name')
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def remove_city(city_id):
    """ remove city """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        if storage_t != "db":
            for place in storage.all(Place).values():
                if place.city_id == city_id:
                    for review in storage.all(Review).values():
                        if review.place_id == place.id:
                            storage.delete(review)
                    storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ update city """
    city = storage.get(City, city_id)
    if city:
        data = request.get_json()
        if not data:
            abort(400, description='Not a JSON')
        for key, value in data.items():
            if key not in ('id', 'state_id', 'created_at', 'updated_at'):
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    abort(404)

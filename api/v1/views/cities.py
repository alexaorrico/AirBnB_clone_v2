#!/usr/bin/python3
"""
view for City objects that handles all default RestFul API actions
"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_cities(state_id):
    """Retrieves the list of all City objects or create a new City object"""
    state_obj = storage.get("State", state_id)
    if state_obj:
        if request.method == 'GET':
            return jsonify([city_obj.to_dict() for city_obj in state_obj.
                            cities]), 200
        if request.method == 'POST':
            if not request.get_json(silent=True):
                abort(400, "Not a JSON")
            if not request.get_json(silent=True).get('name'):
                abort(400, "Missing name")
            kwargs = request.get_json(silent=True)
            new_city = City(**kwargs)
            setattr(new_city, 'state_id', state_id)
            new_city.save()
            return jsonify(new_city.to_dict()), 201
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city_byid(city_id):
    """Retrieves a City object by id, delete or update a City object"""
    city_obj = storage.get("City", city_id)
    if city_obj:
        if request.method == 'GET':
            return jsonify(city_obj.to_dict()), 200
        elif request.method == 'DELETE':
            storage.delete(city_obj)
            storage.save()
            return {}, 200
        elif request.method == 'PUT':
            if not request.get_json(silent=True):
                abort(400, "Not a JSON")
            kwargs = request.get_json(silent=True)
            if kwargs:
                for key, value in kwargs.items():
                    if key not in ["id", "created_at", "updated_at"]:
                        setattr(city_obj, key, value)
                city_obj.save()
            return jsonify(city_obj.to_dict()), 200
    else:
        abort(404)

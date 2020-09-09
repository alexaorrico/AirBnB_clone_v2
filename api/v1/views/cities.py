#!/usr/bin/python3
"""cutty sark"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify


@app_views.route('/api/v1/states/<state_id>/cities')
def get_cities():
    """return list of all cities in state"""
    lizt = []
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    for city in state.cities:
        lizt.append(city.to_dict())
    return jsonify(lizt)


@app_views.route('/api/v1/cities/<city_id>')
def get_a_city():
    """retrieve of specific City object"""
    lizt = []
    urban = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            lizt = city.to_dict()
            return jsonify(lizt)
    return jsonify({"error": "Not found"}), 404

@app_views.route('/api/v1/cities/<city_id>', methods=[DELETE])
def del_a_city():
    """delete a specific city"""
    urban = storage.get(City, city_id)
    if urban is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

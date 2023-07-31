#!/usr/bin/python3
"""
module state.py
"""

from flask import abort, jsonify, request
from models.city import City
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cityObjOfState(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cityList = []
    """same as cities_list = [city.to_dict() for city in state.cities]"""
    for citys in state.cities:
        cityList.append(citys.to_dict())
    return jsonify(cityList)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def cityObj(city_id):
    """Retrieves a City object."""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def cityDeleteWithId(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def createCity(state_id):
    """Creates a City: POST /api/v1/states/<state_id>/cities"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    state = storage.get(State, state_id)
    if state:
        newCityData = request.get_json()
        if not newCityData.get('name'):
            abort(400, description='Not a JSON')

        newCityData['state_id'] = state_id

        newCityObj = City(**newCityData)
        storage.new(newCityObj)
        storage.save()

        return jsonify(newCityObj.to_dict()), 201
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updateCity(city_id):
    """Updates a City object"""
    cityObj = storage.get(City, city_id)
    if cityObj:
        update = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        ignoredKeys = ['id', 'state_id', 'created_at', 'updated_at']
        for k, v in update.items():
            if k not in ignoredKeys:
                setattr(cityObj, k, v)

        storage.save()
        return jsonify(cityObj.to_dict()), 200
    else:
        abort(404)

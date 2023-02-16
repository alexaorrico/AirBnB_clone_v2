#!/usr/bin/python3
"""create a new view for City objects that
   handles all default RESTFul API actions:
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def getCityState(state_id):
    """ gets the cities given the state id """
    CityInState = []
    States = storage.get(State, state_id)
    if States:
        for city in States.cities:
            CityInState.append(city.to_dict())
        return jsonify(CityInState)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def getCity(city_id):
    """ gets the city given the id"""
    CityList = []
    Citys = storage.get(City, city_id)
    if Citys:
        return jsonify(Citys.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def deleteCity(city_id):
    """deletes a city object"""
    Citys = storage.get(City, city_id)
    if Citys:
        storage.delete(Citys)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('states/<state_id>/cities', methods=['POST'],
                strict_slashes=False)
def postCityState(state_id):
    """post to the city"""
    States = storage.get(State, state_id)
    if not States:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    PostDict = request.get_json()
    UpdatedClass = City(**PostDict)
    UpdatedClass.state_id = state_id
    UpdatedClass.save()
    return make_response(jsonify(UpdatedClass.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def PutCity(city_id):
    """ puts to the city object"""
    Citys = storage.get(City, city_id)
    if not Citys:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignoreList = ['id', 'state_id', 'created_at', 'updated_at']
    PutCity = request.get_json()
    for k, v in PutCity.items():
        if k not in ignoreList:
            setattr(Citys, k, v)
    storage.save()
    return make_response(jsonify(Citys.to_dict()), 200)

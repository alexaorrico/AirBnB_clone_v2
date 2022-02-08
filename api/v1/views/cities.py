#!/usr/bin/python3
'''City objects'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def allCities(state_id):
    '''Retrieves the list of all City objects of a State:
    GET /api/v1/states/<state_id>/cities'''
    state = storage.get('State', state_id)
    if state:
        listCities = []
        for city in state.cities:
            listCities.append(city.to_dict())
        return jsonify(listCities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def objCity(city_id):
    '''Retrieves a City object. :
    GET /api/v1/cities/<city_id>'''
    city = storage.get('City', city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def deleteCity(city_id):
    '''Deletes a City object:
    DELETE /api/v1/cities/<city_id>'''
    city = storage.get('City', city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def createCity(state_id):
    '''Creates a City:
    POST /api/v1/states/<state_id>/cities'''
    state = storage.get('State', state_id)
    if state:
        data_request = request.get_json()
        if isinstance(data_request, dict):
            for k in data_request.keys():
                if k == "name":
                    obj = City(**data_request)
                    setattr(obj, 'state_id', state_id)
                    storage.new(obj)
                    storage.save()
                    return jsonify(obj.to_dict()), 201
                else:
                    abort(400, 'Missing name')
        else:
            abort(400, 'Not a JSON')
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updateCity(city_id):
    '''Updates a City object:
    PUT /api/v1/cities/<city_id>'''
    obj = storage.get('City', city_id)
    if obj:
        data_request = request.get_json()
        if isinstance(data_request, dict):
            noKeys = ['id', 'state_id', 'created_at', 'updated_at']
            for key, value in data_request.items():
                if key not in noKeys:
                    setattr(obj, key, value)
            storage.save()
            return jsonify(obj.to_dict()), 200
        else:
            abort(400, 'Not a JSON')
    else:
        abort(404)

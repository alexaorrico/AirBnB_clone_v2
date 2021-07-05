#!/usr/bin/python3
''' Cities viewer '''

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET'], strict_slashes=False)
def getCities(state_id):
    ''' gets all City information used for all states '''
    if storage.get('State', state_id) is None:
        abort(404)
    citiesList = []
    all_city_objs = storage.all(City)
    for city in all_city_objs.values():
        if city.state_id == state_id:
            citiesList.append(city.to_dict())
    return jsonify(citiesList)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def getCity(city_id):
    ''' gets City information for named state '''
    citySelect = storage.get("City", city_id)
    if citySelect is None:
        abort(404)
    return jsonify(citySelect.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteCity(city_id):
    ''' deletes named city based on its city_id '''
    cityDelete = storage.get("City", city_id)
    if cityDelete is None:
        abort(404)
    cityDelete.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/<string:state_id>/cities', methods=['POST'], strict_slashes=False)
def postCity(state_id):
    ''' create a new city '''
    if storage.get('State', state_id) is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    cityPost = City(**request.get_json())
    setattr(cityPost, 'state_id', state_id)
    cityPost.save()
    return make_response(jsonify(cityPost.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def putCity(city_id):
    ''' updates named city '''
    cityUpdate = storage.get("City", city_id)
    print(cityUpdate)
    if cityUpdate is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, value in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(cityUpdate, attr, value)
    cityUpdate.save()
    return jsonify(cityUpdate.to_dict())

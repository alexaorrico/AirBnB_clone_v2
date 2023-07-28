#!/usr/bin/python3
"""City module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from flasgger.utils import swag_from


# GET
@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/get.yml', methods=['GET'])
def get_cities(state_id):
    """Retrieve all City objects"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    all_cities = [obj.to_dict() for obj in state.cities]
    return jsonify(all_cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/city/get_id.yml', methods=['GET'])
def get_city(city_id):
    """Retrieve City object by id"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    return jsonify(city.to_dict())


# DELETE
@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/city/delete.yml', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object by id"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    city.delete()
    storage.save()
    return jsonify({})


# POST
@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/city/post.yml', methods=['POST'])
def create_city(state_id):
    """Creates new City object"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    json_obj = request.get_json()
    obj = City(**json_obj)
    obj.state_id = state.id
    obj.save()
    return jsonify(obj.to_dict()), 201


# PUT
@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/city/put.yml', methods=['PUT'])
def update_city(city_id):
    """Updates City object"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get(City, city_id)

    if obj is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    storage.save()
    return jsonify(obj.to_dict())

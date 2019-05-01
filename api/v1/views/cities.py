"""Routing for AirBnB city object"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>', methods=['GET'])
def get_city(city_id=None):
    """'GET' response"""
    dic = storage.all(City)
    if request.method == 'GET':
        if city_id is None:
            cities_list = []
            for key, value in dic.items():
                cities_list.append(value.to_dict())
            return jsonify(cities_list)
        else:
            for key, value in dic.items():
                if value.id == city_id:
                    return jsonify(value.to_dict())
            abort(404)

@app_views.route('/cities/<city_id>', methods=['GET'])
@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    """'GET' response"""
    dic = storage.all(City)
    if request.method == 'GET':
        if city_id is None:
            cities_list = []
            for key, value in dic.items():
                cities_list.append(value.to_dict())
            return jsonify(cities_list)
        else:
            for key, value in dic.items():
                if value.id == city_id:
                    return jsonify(value.to_dict())
            abort(404)



@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id=None):
    """'DELETE' response"""
    dic = storage.all(City)
    if request.method == 'DELETE':
        empty = {}
        if city_id is None:
            abort(404)
        for key, value in dic.items():
            if value.id == city_id:
                storage.delete(value)
                return jsonify(empty), 200
        abort(404)


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def post_city():
    """'POST' response"""
    dic = storage.all(City)
    flag = 0
    if not request.json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    for key in body:
        if key == 'name':
            flag = 1
    if flag == 0:
        abort(400, "Missing name")
    new_city = City(**body)
    storage.new(new_city)
    storage.save()
    new_city_dic = new_city.to_dict()
    return jsonify(new_city_dic), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city(city_id=None):
    """'PUT' response"""
    dic = storage.all(City)
    if not request.json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    for key, value in dic.items():
        if value.id == city_id:
            for k, v in body.items():
                setattr(value, k, v)
            storage.save()
            return jsonify(value.to_dict()), 200
    abort(404)

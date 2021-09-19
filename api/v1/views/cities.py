#!/usr/bin/python3
""" View Cities """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cityAll(state_id):
    """ Retrieves the list cities """
    ll = []
    state = storage.get("State", str(state_id))
    if state is None:
        abort(404)
    xx = storage.all("City").values()
    for yy in xx:
        if yy.state_id == str(state_id):
            ll.append(yy.to_dict())
    return jsonify(ll)


@app_views.route('/cities/<city_id>', methods=['GET'])
def cityId(city_id):
    """ Retrieves an object  ID """
    yy = storage.get("City", str(city_id))
    if yy is None:
        abort(404)
    return jsonify(yy.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def citiesDel(city_id):
    """ Delete a City  ID"""
    yy = storage.get("City", str(city_id))
    if yy is None:
        abort(404)
    yy.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def citiesPost(state_id):
    """ POST  """
    yy = storage.get("State", str(state_id))
    if yy is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    content = request.get_json()
    content['state_id'] = str(state_id)
    city = City(**content)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_cities(city_id):
    """ Update"""
    x = storage.get("City", str(city_id))
    if x is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    a = ["id", "update_at", "created_at", "state_id"]
    content = request.get_json().items()
    for key, val in content:
        if key not in a:
            setattr(x, key, val)
    x.save()
    return jsonify(x.to_dict()), 200

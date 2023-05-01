#!/usr/bin/python3
""" functions GET, PUT, POST & DELETE """

from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET'])
def get_all(state_id):
    """ get all the states """
    lists = []
    all_states = storage.all(State)
    for i in all_states:
        if all_states[i].id == state_id:
            citi = all_states[i].cities
            for item in citi:
                lists.append(item.to_dict())
            return jsonify(lists)
    abort(404)


@app_views.route('/api/v1/cities/<city_id>', methods=['GET'])
def get_id(city_id):
    """ get status by id """
    citi = storage.get(City, city_id)
    if citi:
        return jsonify(citi.to_dict()), 200
    abort(404)


@app_views.route("/api/v1/cities/<city_id>", methods=['DELETE'])
def del_id(city_id):
    """ delete state by id """
    citi = storage.get(City, city_id)
    storage.delete(citi)
    storage.save()
    if not citi:
        abort(404)
    return ({}), 200


@app_views.route('/api/v1/states/<state_id>/cities', methods=['POST'])
def add():
    """ add city to storage """
    dct = storage.all(State)
    for i in dct:
        if dct[i].id == state_id:
            content = request.get_json()
            if request.json:
                if "name" not in content.keys():
                    return jsonify("Missing name"), 400
                else:
                    content['state_id'] = state_id
                    add_city = City(**content)
                    add_city.save()
                return jsonify(add_city.to_dict()), 201
            return jsonify("Not a JSON"), 400
    abort(404)


@app_views.route('/api/v1/cities/<city_id>', methods=['PUT'])
def update(city_id):
    """ update states and city with id """
    dic = storage.all(City)
    for i in dic:
        if dic[i].id == city_id:
            if request.json:
                ignore = ["id", "update_at", "created_at"]
                content = request.get_json()
                for items in content:
                    if items not in ignore:
                        setattr(dic[i], items, content[items])
                dic[i].save()
                return jsonify(dic[i].to_dict())
            else:
                return jsonify("Not a JSON"), 400
    abort(404)

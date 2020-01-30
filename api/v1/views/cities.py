#!/usr/bin/python3
""" City APIRest
 careful by default it uses get method
"""

from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def list_cities(state_id):
    """ list all cities from specified state
    """
    lista = []
    dic = storage.all('State')
    for key in dic:
        if state_id == dic[key].id:
            cities = dic[key].cities
            for elem in cities:
                lista.append(elem.to_dict())
            return (jsonify(lista))
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def city_id(city_id):
    """ return the city
    """
    dic = storage.all('City')
    for key in dic:
        if city_id == dic[key].id:
            return (jsonify(dic[key].to_dict()))
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def city_delete(city_id):
    """ delete the delete
    """
    dic = storage.all('City')
    for key in dic:
        if city_id == dic[key].id:
            dic[key].delete()
            storage.save()
            return (jsonify({}))
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def add_city(state_id):
    """ create a city of a specified state
    """
    lista = []
    dic = storage.all('State')
    for key in dic:
        if state_id == dic[key].id:
            content = request.get_json()
            if not request.json:
                return (jsonify("Not a JSON"), 400)
            else:
                if "name" not in content.keys():
                    return (jsonify("Missing name"), 400)
                else:
                    content["state_id"] = state_id
                    new_city = City(**content)
                    new_city.save()
                    return jsonify(new_city.to_dict()), 201
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ update specified city
    """
    dic = storage.all('City')
    for key in dic:
        if city_id == dic[key].id:
            if not request.json:
                return (jsonify("Not a JSON"), 400)
            else:
                forbidden = ["id", "update_at", "created_at", "state_id"]
                content = request.get_json()
                for k in content:
                    if k not in forbidden:
                        setattr(dic[key], k, content[k])
                dic[key].save()
                return jsonify(dic[key].to_dict())
    abort(404)

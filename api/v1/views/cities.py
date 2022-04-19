#!/usr/bin/python3
"""new view for City objects that handles all default RESTFul  API"""
from api.v1.views import app_views
from models import storage
from models.city import City
from flask import abort, jsonify, request


@app_views.route('/cities/<city_id>', methods=['GET'])
def listallcities(city_id=None):
    """Retrieves a City object"""
    c = storage.get("City", city_id)
    if c is None:
        abort(404)
    else:
        return (jsonify(city.to_dict()), 200)

@app_views.route('/cities/<city_id>', methods=['DELETE'])
def deletecity(city_id=None):
    """Deletes a City object"""
    c = storage.get("City", city_id)
    if c is None:
        abort(404)
    else:
        city.delete()
        storage.save()
        return (jsonify({}), 200)

@app_views.route('/states/<state_id>/cities', methods=['POST'])
def createcity():
    """Creates a City"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    c = storage.request.get_json("City", silent=True)
    if c == None:
        return (400, "Not a JSON")
    elif "name" not in  c.keys():
        return (400, "Missing name")
    else:
        return (jsonify({}), 201)

@app_views.route('/cities/<city_id>', method=['PUT'])
def updatecity(city_id=None):
    """Updates a City object"""
    ct = storage.get("City", city_id)
    if ct is None:
        abort(404)
    c = request.get_json("City", silent=True)
    if c is None:
        abort(400, "Not a JSON")

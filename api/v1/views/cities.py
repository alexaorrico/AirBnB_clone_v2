#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API"""
from models import storage, city
from flask import abort, jsonify, request


@app_views.route('/cities/<city_id>', methods=['GET'])
def listallcities(city_id=None):
    """list of all State objects"""
    c = storage.get("City", city_id)
    if c == None:
        abort(404)
    else:
        return (jsonify(city.to_dict()), 200)

@app_views.route('/cities/<city_id>', methods=['DELETE'])
def deletecities(city_id=None):
    """Deletes a State object"""
    c = storage.get("City", city_id)
    if c is None:
        abort(404)
    else:
        city.delete()
        storage.save()
        return (jsonify({}), 200)

@app_views.route('/states/<state_id>/cities', methods=['POST'])
def createstate():
    """Creates a State"""
    s = storage.request.get_json("State", silent=True)
    if s == None:
        return (400, "Not a JSON")
    elif "name" not in  s.keys():
        return (400, "Missing name")
    else:
        return (jsonify({}), 201)

@app_views.route('/cities/<city_id>', method=['PUT'])
def updatestate(city_id=None):
    """Updates a State object"""
    ct = storage.get("City", city_id)
    if ct is None:
        abort(404)
    c = storage.request.get_json("State", silent=True)
    if c == None:
        abort(400, "Not a JSON")


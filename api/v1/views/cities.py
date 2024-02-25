#!/usr/bin/python3
"""
Creates a new view for objects for all default API actions
"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.city import City


def getcity(city):
    """Get city"""
    return (city.to_dict(), 200)


def put_city(city):
    """Update city"""
    if not request.is_json:
        abort(400, "Not a JSON")
    new = request.get_json()
    for (k, v) in new.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(city, k, v)
    storage.save()
    return (city.to_dict(), 200)


def delete_city(city):
    """Delete object"""
    storage.delete(city)
    storage.save()
    return ({}, 200)


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities(state_id):
    """Retrieves list of all cities"""
    state = None
    for s in storage.all('State').values():
        if s.id == state_id:
            state = s
    if state is None:
        abort(404)
    if request.method == 'GET':
        all_cities = []
        for x in storage.all('City').values():
            if x.state_id == state_id:
                all_cities.append(x.to_dict())
        return (jsonify(all_cities), 200)
    elif request.method == 'POST':
        if not request.is_json:
            abort(400, "Not a JSON")
        new = request.get_json()
        if 'name' not in new.keys():
            return ({"error": "Missing name"}, 400)
        x = City()
        for (k, v) in new.items():
            setattr(x, k, v)
        setattr(x, 'state_id', state_id)
        x.save()
        return (x.to_dict(), 201)


@app_views.route('/cities/<ident>', methods=['GET', 'PUT', 'DELETE'])
def cities_id(ident):
    """Retrieves a specific city"""
    cities = storage.all("City").values()
    for c in cities:
        if c.id == ident:
            if request.method == 'GET':
                return getcity(c)
            elif request.method == 'PUT':
                return put_city(c)
            elif request.method == 'DELETE':
                return delete_city(c)
    abort(404, 'Not found')

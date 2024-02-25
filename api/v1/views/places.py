#!/usr/bin/python3
"""
Creates a new view for objects for all default API actions
"""
from flask import request, jsonify, abort

from api.v1.views import app_views
from models import storage
from models.place import Place


def getplace(place):
    """Get palce"""
    return (place.to_dict(), 200)


def putplace(place):
    """Update place"""
    if not request.is_json:
        abort(400, "Not a JSON")
    new = request.get_json()
    for (k, v) in new.items():
        if k != 'id' and \
                k != 'created_at' and \
                k != 'updated_at' and \
                k != 'user_id' and \
                k != 'city_id':
            setattr(place, k, v)
    storage.save()
    return (place.to_dict(), 200)


def deleteplace(place):
    """Delete object"""
    storage.delete(place)
    storage.save()
    return ({}, 200)


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places(city_id):
    """Retrieves list of all places"""
    city = None
    for c in storage.all('City').values():
        if c.id == city_id:
            city = c
    if city is None:
        abort(404)
    if request.method == 'GET':
        all_places = []
        for x in storage.all('Place').values():
            if x.city_id == city_id:
                all_places.append(x.to_dict())
        return (jsonify(all_places), 200)
    elif request.method == 'POST':
        if not request.is_json:
            abort(400, "Not a JSON")
        new = request.get_json()
        if 'name' not in new.keys():
            return ({"error": "Missing name"}, 400)
        if 'user_id' not in new.keys():
            return ({"error": "Missing user_id"}, 400)
        user_id = new['user_id']
        y = [x.id for x in storage.all('User').values()]
        if user_id not in y:
            abort(404)
        x = Place()
        for (k, v) in new.items():
            setattr(x, k, v)
        setattr(x, 'city_id', city_id)
        x.save()
        return (x.to_dict(), 201)


@app_views.route('/places/<ident>', methods=['GET', 'PUT', 'DELETE'])
def places_id(ident):
    """Retrieves a specific place"""
    places = storage.all("Place").values()
    for p in places:
        if p.id == ident:
            if request.method == 'GET':
                return getplace(p)
            elif request.method == 'PUT':
                return putplace(p)
            elif request.method == 'DELETE':
                return deleteplace(p)
    abort(404, 'Not found')

#!/usr/bin/python3
""" View Place """

import models
from flask import jsonify, abort
from flask import request as req
from models.place import Place
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def place_objects(city_id):
    """id city retrieve json object with his places"""
    city = models.storage.get('City', city_id)
    if city is None:
        abort(404)

    if req.method == 'GET':
        places = [obj.to_dict() for obj in city.places]
        return jsonify(places)

    if req.method == 'POST':
        reqj = req.get_json()
        if reqj is None:
            abort(400, 'Not a JSON')
        if reqj.get('name', None) is None:
            abort(400, 'Missing name')
        if reqj.get('user_id', None) is None:
            abort(400, 'Missing user_id')

        user = models.storage.get('User', reqj.get('user_id'))
        if user is None:
            abort(404)

        place = Place(**reqj)
        place.city_id = city_id
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'])
def place_res(place_id):
    """id place retrieve json object"""
    place = models.storage.get('Place', place_id)
    if place is None:
        abort(404)

    if req.method == 'GET':
        return jsonify(place.to_dict())

    if req.method == 'PUT':
        place_json = req.get_json()
        if place_json is None:
            abort(400, 'Not a JSON')
        ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, val in place_json.items():
            if key not in ignore:
                place.__setattr__(key, val)
        models.storage.save()
        return jsonify(place.to_dict())

    if req.method == 'DELETE':
        place.delete()
        models.storage.save()
        return jsonify({})


@app_views.route('/places_search', methods=['POST'])
def place_search():
    reqj = req.get_json()
    if reqj is None:
        abort(400, 'Not a JSON')

    places_dict = models.storage.all('Place')

    state_ids = reqj.get('states', [])
    city_ids = reqj.get('cities', [])
    amenity_ids = reqj.get('amenities', [])
    if not reqj or (not state_ids and not city_ids and not amenity_ids):
        places = [p.to_dict() for p in places_dict.values()]
        return jsonify(places)

    states = []
    if state_ids:
        states = [st for st in models.storage.all('State').values()
                  if st.id in state_ids]

    for st in states:
        [city_ids.append(ct.id) for ct in st.cities]

    city_ids = list(set(city_ids))
    places_list = []
    for ct_id in city_ids:
        [places_list.append(p) for p in places_dict.values()
         if p.city_id == ct_id]

    if not city_ids:
        places_list = list(places_dict.values())

    places = []
    for p in places_list:
        has_all = True
        ids = [a.id for a in p.amenities]
        for am_id in amenity_ids:
            if am_id not in ids:
                has_all = False
                break
        if has_all:
            del p.amenities
            del p.reviews
            places.append(p.to_dict())

    return jsonify(places)

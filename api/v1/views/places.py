#!/usr/bin/python3
"""
handles REST API actions for place
"""
from api.v1.views import app_views
from flask import jsonify
from flask import Flask
from flask import request
from flask import abort
from os import getenv
from models import storage
from models.place import Place


@app_views.route(
    'cities/<string:city_id>/places',
    methods=['GET', 'POST'],
    strict_slashes=False)
def place(city_id):
    """handles places route"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(
            [obj.to_dict() for obj in city.places])
    if request.method == 'POST':
        post_data = request.get_json()
        if post_data is None or type(post_data) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        new_name = post_data.get('name')
        new_user = post_data.get('user_id')
        if new_user is None:
            return jsonify({'error': 'Missing user_id'}), 400
        if storage.get("User", new_user) is None:
            abort(404)
        if new_name is None:
            return jsonify({'error': 'Missing name'}), 400
        new_place = Place(city_id=city_id, **post_data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route(
    '/places/<string:place_id>',
    methods=['GET', 'DELETE', 'PUT'],
    strict_slashes=False)
def place_with_id(place_id):
    """handles places route with a parameter place_id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        put_data = request.get_json()
        if put_data is None or type(put_data) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        to_ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        place.update(to_ignore, **put_data)
        return jsonify(place.to_dict()), 200


@app_views.route(
    '/places_search',
    methods=['POST'],
    strict_slashes=False)
def places_search():
    """searches for places using the posted http_body"""
    post_data = request.get_json()
    places_search = []
    if post_data is None or type(post_data) != dict:
        return jsonify({'error': 'Not a JSON'}), 400
    place = storage.all('Place').values()
    if len(post_data) == 0:
        return jsonify([x.to_dict() for x in place])
    state_ids = post_data.get('states')
    if state_ids is None:
        state_ids = []
    city_ids = post_data.get('cities')
    if city_ids is None:
        city_ids = []
    amen_ids = post_data.get('amenities')
    if amen_ids is None:
        amen_ids = []
    if len(state_ids) == 0 and len(city_ids) == 0 and len(amenity_ids) == 0:
        return jsonify([x.to_dict() for x in place])
    for c in city_ids:
        city = storage.get('City', c)
        if city is not None:
            for p in city.places and p.to_dict() not in places_search:
                places_search.append(p.to_dict())
    for s in state_ids:
        state = storage.get('State', s)
        if state is not None:
            for cit in state.cities:
                if cit.id not in city_ids:
                    for pla in cit.places:
                        if pla.to_dict() not in places_search:
                            places_search.append(pla.to_dict())
    for p in place:
        if len(amen_ids) == 0:
            break
        all_match = True
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            for ids in amen_ids:
                if ids not in p.amenity_ids:
                    all_match = False
                    break
        else:
            for ids in amen_ids:
                cur_amenity = storage.get('Amenity', ids)
                if cur_amenity is None or cur_amenity not in p.amenities:
                    all_match = False
                    break
        if all_match is True and p.to_dict() not in places_search:
            places_search.append(p.to_dict())
    return jsonify(places_search)

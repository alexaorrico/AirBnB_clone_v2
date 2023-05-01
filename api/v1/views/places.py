#!/usr/bin/python3

'''
Create a new view for City objects that handles
all default RestFul API actions.
'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from api.v1.views import get, delete, post, put
from models import storage
import os


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def place_crud(city_id=None, place_id=None):
    '''Returns GET, DELETE, PUT, POST methods'''
    data = {
            'str': 'Place',
            '_id': place_id,
            'p_id': city_id,
            'p_prop': 'city_id',
            'p_child': 'places',
            'p_str': 'City',
            'check': ['user_id', 'name'],
            'ignore': ['created_at', 'updated_at', 'id', 'user_id', 'city_id']}
    methods = {
            'GET': get,
            'DELETE': delete,
            'POST': post,
            'PUT': put
            }
    if request.method in methods:
        return methods[request.method](data)


@app_views.route('/places_search',
                 strict_slashes=False,
                 methods=['POST'])
def search_crud():
    ''' Filters places by state, city, and amenities '''
    req = request.get_json()
    if req is None:
        return jsonify({'error': 'Not a JSON'}), 400
    places = storage.all("Place").values()
    if req == {}:
        return jsonify([x.to_dict() for x in places]), 200
    state_list = check_and_get(req, 'states', 'State')
    city_list = populate(state_list, 'cities') |\
        check_and_get(req, 'cities', 'City')
    place_list = populate(city_list, 'places') if len(city_list) else places
    if not req.get('amenities') or len(req['amenities']) == 0:
        return jsonify([x.to_dict() for x in place_list]), 200
    amenity_list = check_and_get(req, 'amenities', 'Amenity', True)
    return filter_results(place_list, amenity_list)


def check_and_get(req, cls_str, cls, id_only=False):
    ''' Checks db for class according to list of id's '''
    _set = set()
    cls_array = req.get(cls_str)
    if cls_array:
        for _id in cls_array:
            found = storage.get(cls, _id)
            if id_only:
                _set.add(found.id)
            elif found:
                _set.add(found)
    return _set


def populate(parent_list, child_prop):
    ''' Populate subclasses of a parent list of classes'''
    _set = set()
    for p in parent_list:
        for child in getattr(p, child_prop):
            _set.add(child)
    return _set


def filter_results(place_list, amenity_list):
    ''' Filter results of place list with specified amenities '''
    filtered = []
    for place in place_list:
        required_amens = [a.id for a in place.amenities]
        if required_amens and all([x in required_amens for x in amenity_list]):
            filtered.append(place)
    return jsonify([x for x in remove_subclass(filtered, 'amenities')]), 200


def remove_subclass(_list, subclass):
    ''' Remove subclasses for serialization '''
    res = []
    for _ in _list:
        d = _.to_dict()
        del d[subclass]
        res.append(d)
    return res

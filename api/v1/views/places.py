#!/usr/bin/python3
"""
New view for Places objects that handles all default RestFul API actions.
"""
from models.place import Place
from models.city import City
from models import storage
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views


@app_views.route('/places', strict_slashes=False, methods=['GET'])
def all_places():
    '''
    Retrieves the list of all Place objects
    '''
    Places_List = []
    for value in storage.all('Place').values():
        Places_List.append(value.to_dict())
    return jsonify(Places_List)


@app_views.route('/cities', strict_slashes=False, methods=['GET'])
def all_cities():
    '''
    Retrieves the list of all Citiy objects 
    '''
    Cities_List = []
    for value in storage.all('City').values():
        Cities_List.append(value.to_dict())
    return jsonify(Cities_List)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def all_places_of_a_city(city_id):
    '''
    Retrieves the list of all Place objects of a City
    '''
    Places_List = []
    City_Storage = storage.get('City', city_id)
    if not City_Storage:
        abort(404)
    for city in storage.all('Place').values():
        if city.to_dict()["city_id"] == city_id:
            Places_List.append(city.to_dict())
    return jsonify(Places_List)


@app_views.route('/places/<place_id>', methods=['GET'])
def specific_place(place_id):
    '''
    Retrieves a Place object
    '''
    Place_Storage = storage.get("Place", place_id)
    if Place_Storage is None:
        abort(404)
    return jsonify(Place_Storage.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ Deletes a Place object. """
    Place_Storage = storage.get('Place', place_id)
    if Place_Storage:
        storage.delete(Place_Storage)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """ Creates a Place. """
    dic = request.get_json()
    City_Storage = storage.get('City', city_id)
    User_Storage = storage.get('User', dic["user_id"])
    if not City_Storage:
        abort(404)
    if not User_Storage:
        abort(404)
    if not dic:
        abort(400, {'Not a JSON'})
    if 'name' not in dic:
        abort(400, {'Missing name'})
    if 'user_id' not in dic:
        abort(400, {'Missing user_id'})
    new_place = Place(**dic)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def updates_place(place_id):
    """ Updates a Place object. """
    dic = request.get_json()
    Selected_Review = storage.get('Place', place_id)
    if not Selected_Review:
        abort(404)
    if not dic:
        abort(400, {'Not a JSON'})
    for key, value in dic.items():
        if key not in ['id', 'user_id', 'city_id', 'updated_at', 'created_at']:
            setattr(Selected_Review, key, value)
    storage.save()
    return jsonify(Selected_Review.to_dict()), 200

#!/usr/bin/python3
'''
API for Place
'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
import models


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_city_places(city_id):
    '''Returns all place object by city_id in json format'''
    json_list = []

    place_list = storage.get('City', city_id)
    if place_list is None:
        abort(404)
    for place in place_list.places:
        json_list.append(place.to_dict())
    return jsonify(json_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    '''Retrieves a Place from storage'''
    try:
        place = storage.get('Place', place_id).to_dict()
        return jsonify(place)
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''Deletes a City from storage'''
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


def attrib_update(obj, **args):
    '''Helper function to update objects attributes to correct types'''
    for key, value in args.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            if hasattr(obj, key):
                if isinstance(value, str):
                    value = value.replace("_", " ")
                setattr(obj, key, value)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    '''Creates an instance of Amenity and save it to storage'''
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    form = request.get_json(force=True)
    user_id_check = form.get('user_id')
    if user_id_check is None:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get('User', form['user_id'])
    if user is None:
        abort(404)
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    place_class = models.classes['Place']
    new_place = place_class(**form)
    setattr(new_place, 'city_id', city_id)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places_search', methods=['POST'])
def search_places():
    '''
    Searches places depending on:
    states id - all places in states
    cities id - all places in cities
    amenities id - print only places with the following amenities
    '''
    form = request.get_json(force=True)
    place_list = []
    all_cities = []
    all_amenities = []
    all_place = []
    if len(form) == 0:
        all_place = storage.all('Place')
        for place in all_place.values():
            place_list.append(place.to_dict())
        return jsonify(place_list), 200
    if 'cities' in request.json:
        for city_id in form['cities']:
            all_cities.append(storage.get('City', city_id))
    if 'states' in request.json:
        for state_id in form['states']:
            for city in storage.get('State', state_id).cities:
                if city not in all_cities:
                    all_cities.append(city)
    for city in all_cities:
        for place in city.places:
                all_place.append(place)

    if 'amenities' in request.json and len(all_place) != 0:
        for amenity_id in form['amenities']:
            all_amenities.append(storage.get('Amenity', amenity_id))
        for amenity in all_amenities:
            for place in all_place:
                if place not in amenity.place_amenities:
                    all_place.remove(place)
    if 'amenities' in request.json and len(all_place) == 0:
        for amenity_id in form['amenities']:
            all_amenities.append(storage.get('Amenity', amenity_id))
        for amenity in all_amenities:
            for place in amenity.place_amenities:
                place_list.append(place.to_dict())
        return jsonify(place_list), 200

    for place in all_place:
        place_list.append(place.to_dict())
    return jsonify(place_list), 200


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    '''Updates Amenity object attribute'''
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    form = request.get_json(force=True)
    if form is None:
        abort(400, "Not a JSON")
    attrib_update(place, **form)
    place.save()
    return jsonify(place.to_dict()), 200

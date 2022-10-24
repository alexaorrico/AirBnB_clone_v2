#!/usr/bin/python3
"""
view for Place  objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places')
def get_cities_of_places(city_id):
    """Retrieves the list of all Place objects linked to a City"""
    city = storage.get(City, city_id)
    places = storage.all(Place)
    if not city:
        abort(404)
    city_places = [
        place.to_dict()
        for place in places.values() if place.city_id == city_id
        ]
    return jsonify(city_places)


@app_views.route('/places/<place_id>')
def get_place(place_id):
    """"Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    all_places = storage.all(Place)
    if not place:
        abort(404)
    for k, v in all_places.items():
        if v.id == place_id:
            v.delete()
            storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def add_place(city_id):
    """creates a Place (linked to a City by id)"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON\n", 400)
    if 'name' not in request.get_json():
        return ("Missing name\n", 400)
    if 'user_id' not in request.get_json():
        return ("Missing user_id\n", 400)
    else:
        if 'user_id' in request.get_json():
            user = storage.get(User, request.get_json()['user_id'])
            if not user:
                abort(404)
    request_data = request.get_json()
    request_data['user_id'] = user.id
    request_data['city_id'] = city_id
    new_place = Place(**request_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """updates a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON\n", 400)
    request_data = request.get_json()
    request_data.pop('id', None)
    request_data.pop('user_id', None)
    request_data.pop('city_id', None)
    request_data.pop('created_at', None)
    request_data.pop('updated_at', None)
    for key in request_data:
        setattr(place, key, request_data[key])
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """places search"""
    places = [place.to_dict() for place in storage.all(Place).values()]
    request_data = request.get_json(force=True, silent=True)
    if not request_data and request_data != {}:
        return ("Not a JSON\n", 400)
    data = [val for val in request_data.values() if len(val) != 0]
    if not data:
        return jsonify(places)
    results = []
    for key, value in request_data.items():
        if key == 'states':
            for id in value:
                for city in storage.get(State, id).cities:
                    for place in city.places:
                        results.append(place)
        if key == 'cities':
            for id in value:
                for place in storage.get(City, id).places:
                    results.append(place)
        if key == 'amenities':
            amn_results = []
            if len(results) != 0:
                for place in results:
                    amn_ids = [amn.id for amn in place.amenities]
                    if set(value).issubset(amn_ids):
                        amn_results.append(place)
                amn_results = set(amn_results)
                # for place in amn_results:
                #     print('-------')
                #     for i in place.amenities:
                #         print(i.name)
                amn_results = [place.to_dict() for place in amn_results]
                for place in amn_results:
                    del place['amenities']
                return jsonify(amn_results)
            else:
                # print('ok')
                for place in storage.all(Place).values():
                    # print('here')
                    amn_ids = [amn.id for amn in place.amenities]
                    # print(amn_ids)
                    # print(value)
                    if set(value).issubset(amn_ids):
                        # print('found')
                        amn_results.append(place)
                amn_results = set(amn_results)
                amn_results = [place.to_dict() for place in amn_results]
                for place in amn_results:
                    del place['amenities']
                return jsonify(amn_results)

    results = set(results)
    # print(results)
    results = [place.to_dict() for place in results]
    # for i in results:
    # print(results)
    return jsonify(results)

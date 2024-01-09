#!/usr/bin/python3
''' REST API blueprint for Place class '''

from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.place import Place
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place_by_city(city_id):
    ''' Find and returns places in city using city_d '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places_list = [place.to_dict() for place in city.places]
    return (jsonify(places_list), 200)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    ''' returns place with matching id '''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    ''' Deletes place object with given place_id '''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place_by_city_id(city_id):
    ''' creates new place object through city id '''
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    elif "user_id" not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    else:
        user_id = data['user_id']
        user = storage.get("User", user_id)
        city = storage.get("City", city_id)
        if city is None or user is None:
            abort(404)
        data['user_id'] = user.id
        data['city_id'] = city.id
        obj = Place(**data)
        obj.save()
        return (jsonify(obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    ''' updates existing place object with maching id '''
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "user_id", "created_at", "updated_at"]:
            setattr(obj, key, value)
    obj.save()
    return (jsonify(obj.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_by_post():
    """ searches for a place using list of ids """
    ids = request.get_json()
    if not ids:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    else:
        state_ids = ids.get('states', [])
        city_ids = ids.get('cities', [])
        amenity_ids = ids.get('amenities', [])
        if state_ids == city_ids == amenity_ids == []:
            places = storage.all("Place").values()
        elif state_ids != []:
            places = []
            for state_id in state_ids:
                state = storage.get("State", state_id)
                if state is not None:
                    cities = state.cities
                else:
                    cities = []
                [city_ids.append(city.id) for city in cities if
                    city.id not in city_ids]
            for city_id in city_ids:
                city = storage.get("City", city_id)
                if city is not None:
                    [places.append(place) for place in city.places]
        amenities = [storage.get('Amenity', amenity_id)
                     for amenity_id in amenity_ids if
                     storage.get('Amenity', amenity_id)]
        unique_place_list = []
        for place in places:
            unique_place_list.append(place.to_dict())
            place_amenities = place.amenities
            for amenity in amenities:
                if amenity not in place_amenities:
                    unique_place_list.pop()
                    break
        return jsonify(unique_place_list)

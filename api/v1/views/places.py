#!/usr/bin/python3
"""
This is module places
"""
from api.v1.views import (app_views, Place, storage)
from flask import (abort, jsonify, make_response, request)
import os


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def view_places_in_city(city_id):
    """Example endpoint returns a list of all places in a city
    Retrieves all places within a city
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    result = [place.to_json() for place in city.places]
    return jsonify(result)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def view_place(place_id=None):
    """Example endpoint returns a single plac
    """
    s = storage.get("Place", place_id)
    if s is None:
        abort(404)
    return jsonify(s.to_json())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """Example endpoint deleting one place
    Deletes a place based on the place_id of the JSON body
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Example endpoint creates a single place
    Create a single place based on the JSON body
     """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    if 'user_id' not in r.keys():
        return "Missing user_id", 400
    user = storage.get("User", r.get("user_id"))
    if user is None:
        abort(404)
    if 'name' not in r.keys():
        return "Missing name", 400
    r["city_id"] = city_id
    s = Place(**r)
    s.save()
    return jsonify(s.to_json()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    """Example endpoint creates a single place
    Updates a place based on the JSON
    """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    a = storage.get("Place", place_id)
    if a is None:
        abort(404)
    for k in ("id", "user_id", "city_id", "created_at", "updated_at"):
        r.pop(k, None)
    for k, v in r.items():
        setattr(a, k, v)
    a.save()
    return jsonify(a.to_json()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def list_places():
    """Example endpoint list all places of a JSON body
    Retrieves a list of all places
     """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    if not r:
        return jsonify([e.to_json() for e in storage.all("Place").values()])

    all_cities_id = r.get("cities", [])
    states = r.get("states")
    if states:
        all_states = [storage.get("State", s) for s in states]
        all_states = [a for a in all_states if a is not None]
        all_cities_id += [c.id for s in all_states for c in s.cities]
    all_cities_id = list(set(all_cities_id))

    all_amenities = r.get("amenities")
    all_places = []
    if all_cities_id or all_amenities:
        all_places2 = storage.all("Place").values()
        if all_cities_id:
            all_places2 = [p for p in all_places2 if
                           p.city_id in all_cities_id]
        if all_amenities:
            if os.getenv('HBNB_TYPE_STORAGE', 'fs') != 'db':
                all_places = [p for p in all_places2 if
                              set(all_amenities) <= set(p.amenities_id)]
            else:
                for e in all_places2:
                    flag = True
                    for a in all_amenities:
                        if a not in [i.id for i in e.amenities]:
                            flag = False
                            break
                    if flag:
                        all_places.append(e)
        else:
            all_places = all_places2
    return jsonify([p.to_json() for p in all_places])

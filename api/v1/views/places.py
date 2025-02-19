#!/usr/bin/python3
"""
Module creates an api view for Place objects
"""

from flask import jsonify, abort, request
from api.v1.views.__init__ import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from os import getenv

storage_t = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def city_to_place_index(city_id):
    """
    Retrieves all places under city city_id on
    GET /api/v1/cities/<city_id>/places
    """
    parent_obj = storage.get(City, city_id)
    if parent_obj is None:
        abort(404)
    else:
        all_places_raw = parent_obj.places
        all_places = []
        for place in all_places_raw:
            all_places.append(place.to_dict())
        return jsonify(all_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_by_id(place_id):
    """
    Retrieves place object by its id on
    GET /api/v1/places/<place_id>
    """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """
    Deletes a place object on
    DELETE /api/v1/places/<place_id> request
    """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """
    Replaces a place object on
    PUT /api/v1/places/<place_id> request
    """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)

    else:
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            abort(400, description='Not a JSON')
        else:
            json = request.get_json()
            if json is None:
                abort(400, description='Not a JSON')
            for key, value in json.items():
                if key not in [
                    'id', 'user_id', 'city_id', 'created_at', 'updated_at'
                ]:
                    setattr(obj, key, value)
                obj.save()
            return place_by_id(place_id), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """
    Posts a place object and adds it to its parent city
    POST /api/v1/cities/<city_id>/places request
    """
    parent_obj = storage.get(City, city_id)
    if parent_obj is None:
        abort(404)

    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        abort(400, description='Not a JSON')
    else:
        json = request.get_json()
        if json is None:
            abort(400, description='Not a JSON')
        if 'name' not in json.keys():
            abort(400, description='Missing name')
        elif 'user_id' not in json.keys():
            abort(400, description='Missing user_id')

        all_users = list(storage.all(User).values())
        all_user_ids = list(user.id for user in all_users)

        if json['user_id'] not in all_user_ids:
            abort(404)
        else:
            obj = Place(**json)
            obj.city_id = city_id
            obj_id = obj.id
            obj.save()
            return place_by_id(obj_id), 201


@app_views.route("/places_search", methods=['POST'], strict_slashes=False)
def place_search():
    """
    Retrieves all Place objecs depending on the JSON of the
    POST /api/v1/places_search
    """
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        abort(400, description='Not a JSON')
    json = request.get_json()
    if json is None:
        abort(400, description='Not a JSON')
    if len(list(json.keys())) == 0:
        """
        If dictionary is empty return all places
        """
        all_places_raw = list(storage.all(Place).values())
        all_places = [place.to_dict() for place in all_places_raw]
        return jsonify(all_places)

    """if values:list are all empty retrieves all PLaces"""
    st_list = json['states'] if json.get('states') is not None else []
    ct_list = json['cities'] if json.get('cities') is not None else []
    am_list = json['amenities'] if json.get('amenities') is not None else []
    if len(st_list) == 0 and len(ct_list) and len(am_list) == 0:
        all_places_raw = list(storage.all(Place).values())
        all_places = [place.to_dict() for place in all_places_raw]
        return jsonify(all_places)

    """A set will be implemented to avoid duplication"""
    cities_selected = set()
    selected_places = set()
    if len(st_list) != 0 and len(ct_list) == 0:
        for state_id in st_list:
            state_obj = storage.get(State, state_id)
            state_cities = state_obj.cities
            for city in state_cities:
                cities_selected.add(city)

    elif len(st_list) == 0 and len(ct_list) != 0:
        for city_id in ct_list:
            cities_selected.add(storage.get(City, city_id))

    elif len(st_list) != 0 and len(ct_list) != 0:
        for state_id in st_list:
            state_obj = storage.get(State, state_id)
            state_cities_ids = [st.id for st in state_obj.cities]
            if all(ct_id not in state_cities_ids for ct_id in ct_list) is True:
                cities_selected.update(list(state_obj.cities))

            else:
                for ct_id in state_cities_ids:
                    if ct_id in ct_list:
                        cities_selected.add(storage.get(City, ct_id))
        for ct_id in ct_list:
            cities_selected.add(storage.get(City, ct_id))

    """Then we will filter for places in the cities"""
    for city in cities_selected:
        for place in city.places:
            if storage_t == 'file':
                if all(am_id in place.amenities for am_id in am_list):
                    selected_places.add(place.to_dict())
            elif storage_t == 'db':
                place_amenities_id = [am.id for am in place.amenities]
                if all(am_id in place_amenities_id for am_id in am_list):
                    selected_places.add(place.to_dict())

    return jsonify(selected_places)

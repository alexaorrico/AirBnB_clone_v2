#!/usr/bin/python3
"""Places API routes"""
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.place import Place


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def show_places(city_id):
    """Shows all places associated with a city
       Args:
           city_id (str): city uuid
       Returns:
           A list of JSON dictionaries of all places in a city
    """
    city = storage.get('City', city_id)
    places_list = []
    if city:
        for place in city.places:
            places_list.append(place.to_dict())
        return jsonify(places_list)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def show_place(place_id):
    """Shows place
       Args:
           place_id (str): place uuid
       Returns:
           JSON dictionary of place
    """
    place = storage.get('Place', place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route(
    '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes place
       Args:
           place_id (str): place uuid
       Returns:
           Empty JSON dictionary if successful otherwise 404 error
    """
    place = storage.get('Place', place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route(
    '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a place
       Args:
           city_id (str): city uuid
       Returns:
           JSON dictionary of place if successful
    """
    city = storage.get('City', city_id)
    error_message = ""
    if city:
        content = request.get_json(silent=True)
        if type(content) is dict:
            if "user_id" in content.keys():
                user = storage.get('User', content['user_id'])
                if user:
                    if "name" in content.keys():
                        place = Place(**content)
                        place.city_id = city_id
                        storage.new(place)
                        storage.save()
                        response = jsonify(place.to_dict())
                        response.status_code = 201
                        return response
                    else:
                        error_message = "Missing name"
                else:
                    abort(404)
            else:
                error_message = "Missing user_id"
        else:
            error_message = "Not a JSON"

        response = jsonify({"error": error_message})
        response.status_code = 400
        return response
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a place
       Args:
           place_id (str): place uuid
       Returns:
           JSON dictionary of place if successful
    """
    place = storage.get('Place', place_id)
    if place:
        content = request.get_json(silent=True)
        if type(content) is dict:
            ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            for name, value in content.items():
                if name not in ignore:
                    setattr(place, name, value)
            storage.save()
            return jsonify(place.to_dict())

        else:
            response = jsonify({"error": "Not a JSON"})
            response.status_code = 400
            return response
    else:
        abort(404)


@app_views.route('/places_search/', methods=['POST'], strict_slashes=False)
def search_places():
    places_list = []
    place_dicts = []
    cities_list = []
    removal_list = []
    empty = True
    content = request.get_json(silent=True)

    if type(content) is dict:
        for key, value in content.items():
            if len(content[key]) > 0:
                empty = False

        if len(content) == 0 or empty is True:
            places = storage.all('Place').values()
            for place in places:
                place_dicts.append(place.to_dict())

        if "states" in content:
            for state in content["states"]:
                state_obj = storage.get("State", state)
                if state_obj:
                    for city in state_obj.cities:
                        cities_list.append(city)

        if "cities" in content:
            for city in content["cities"]:
                city_obj = storage.get("City", city)
                if city_obj:
                    cities_list.append(city_obj)

        for city in cities_list:
            for place in city.places:
                places_list.append(place)

        if "amenities" in content:
            for place in places_list:
                for amenity in content["amenities"]:
                    amenity_obj = storage.get("Amenity", amenity)
                    if amenity_obj:
                        if amenity_obj not in place.amenities:
                            removal_list.append(place)
                            break

        for place in removal_list:
            if place in places_list:
                places_list.remove(place)

        for place in places_list:
            place_dicts.append(place.to_dict())

        return jsonify(place_dicts)

    else:
        response = jsonify({"error": "Not a JSON"})
        response.status_code = 400
        return response

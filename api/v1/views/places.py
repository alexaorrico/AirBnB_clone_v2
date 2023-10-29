#!/usr/bin/python3
""" Module containing Place View """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, storage_t
from models.place import Place


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Place objects of a City.

        Args:
            city_id (str): The UUID4 string representing a City object.

        Returns:
            List of dictionaries representing Place objects in JSON format.
            Raise 404 error if `city_id` is not linked to any City object.
    """
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    places = [place.to_dict() for place in city_obj.places]
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object based on `place_id`.

    Args:
        place_id (str): The UUID4 string representing a Place object.

    Returns:
        Dictionary represention of a Place object in JSON format.
        Raise 404 error if `place_id` is not linked to any Place object.
    """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object based on `place_id`.

    Args:
        place_id (str): The UUID4 string representing a Place object.

    Returns:
        Returns an empty dictionary with the status code 200.
        Raise 404 error if `place_id` is not linked to any Place object.
    """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    place_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def add_place(city_id):
    """ Creates a Place object using `city_id` and HTTP body request fields.

    Args:
        city_id (str): The UUID4 string representing a City object.

    Returns:
        Returns the new Place object as a  dictionary in JSON format
        with the status code 200.
        Raise 404 error if `state_id` is not linked to any State object.
    """
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    if fields.get('user_id') is None:
        return "Missing user_id", 400
    user_obj = storage.get("User", fields['user_id'])
    if user_obj is None:
        abort(404)
    if fields.get('name') is None:
        return "Missing name", 400
    fields['city_id'] = city_id
    new_place = Place(**fields)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def edit_place(place_id):
    """ Edit a Place object using `place_id` and HTTP body request fields.

    Args:
        place_id (str): The UUID4 string representing a Place object.

    Returns:
        Returns the Place object as a  dictionary in JSON format with the
        status code 200.
        Raise 404 error if `place_id` is not linked to any Place object.
    """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    for key in fields:
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'update_at']:
            if hasattr(place_obj, key):
                setattr(place_obj, key, fields[key])
    place_obj.save()
    return jsonify(place_obj.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def filter_places():
    """ Filter Places based on optional JSON keys passed through HTTP body
        request.

    Returns:
        List of dictionaries representing Place objects.
        400 error if JSON was not passed.
    """
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    states = fields.get('states', [])
    cities = fields.get('cities', [])
    amenities = fields.get('amenities', [])
    places = set()
    if fields == {} or (states == [] and cities == []):
        places = set(storage.all("Place").values())
    for state_id in states:
        state = storage.get('State', state_id)
        if state is not None:
            for city in state.cities:
                for place in city.places:
                    places.add(place)
    for city_id in cities:
        city = storage.get('City', city_id)
        if city is not None:
            for place in city.places:
                places.add(place)
    if amenities != []:
        amenities = set(amenities)
        temp = set()
        for amenity_id in amenities:
            if storage.get("Amenity", amenity_id) is not None:
                temp.add(amenity_id)
        amenities = temp
        to_remove = set()
        for place in places:
            if storage_t == 'db':
                amenities_id = {amenity.id for amenity in place.amenities}
            else:
                amenities_id = set(place.amenity_ids)
            if not set(amenities).issubset(amenities_id):
                to_remove.add(place)
            del place.amenities
        places -= to_remove
    return jsonify([place.to_dict() for place in places])

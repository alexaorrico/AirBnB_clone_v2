#!/usr/bin/python3
""" Module containing City View """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """ Retrieves the list of all City objects of a State.

        Args:
            state_id (str): The UUID4 string representing a State object.

        Returns:
            List of dictionaries representing City objects in JSON format.
            Raise 404 error if `state_id` is not linked to any State object.
    """
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    cities = [city.to_dict() for city in state_obj.cities]
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ Retrieves a City object based on `city_id`.

    Args:
        city_id (str): The UUID4 string representing a City object.

    Returns:
        Dictionary represention of a City object in JSON format.
        Raise 404 error if `city_id` is not linked to any City object.
    """
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object based on `city_id`.

    Args:
        city_id (str): The UUID4 string representing a City object.

    Returns:
        Returns an empty dictionary with the status code 200.
        Raise 404 error if `city_id` is not linked to any City object.
    """
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    city_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def add_city(state_id):
    """ Creates a City object using `state_id` and HTTP body request fields.

    Args:
        state_id (str): The UUID4 string representing a State object.

    Returns:
        Returns the new City object as a  dictionary in JSON format
        with the status code 200.
        Raise 404 error if `state_id` is not linked to any State object.
    """
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    if fields.get('name') is None:
        return "Missing name", 400
    fields['state_id'] = state_id
    new_city = City(**fields)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def edit_city(city_id):
    """ Edit a City object using `city_id` and HTTP body request fields.

    Args:
        city_id (str): The UUID4 string representing a City object.

    Returns:
        Returns the City object as a  dictionary in JSON format with the
        status code 200.
        Raise 404 error if `city_id` is not linked to any City object.
    """
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    for key in fields:
        if key in ['id', 'state_id', 'created_at', 'update_at']:
            continue
        if hasattr(city_obj, key):
            setattr(city_obj, key, fields[key])
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200

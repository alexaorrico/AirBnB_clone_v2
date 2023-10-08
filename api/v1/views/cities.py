#!/usr/bin/python3
"""Create a view for city"""

from flask import request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def citiesByState(state_id):
    """returns a list of all City object
    linked to State object with id = @state_id"""
    stateObj = storage.get(State, state_id)
    if not stateObj:
        abort(404)
    return [cityObj.to_dict() for cityObj in stateObj.cities]


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def getCity(city_id):
    """Get City object linked with id @city_id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return city.to_dict()


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteCity(city_id):
    """Deletes City object with id = @city_id"""
    cityObj = storage.get(City, city_id)
    if cityObj is None:
        abort(404)
    cityObj.delete()
    storage.save()
    return {}, 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def createCity(state_id):
    """Create a new City object.
    Name should be gotten from request.
    """
    stateObj = storage.get(State, state_id)
    if not stateObj:
        abort(404)
    rawCity = request.get_json()
    if not rawCity:
        abort(400, 'Not a JSON')
    if not rawCity.get('name'):
        abort(400, 'Missing name')
    cityObj = City()
    cityObj.state_id = state_id
    for key, value in rawCity.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(cityObj, key, value)
    cityObj.save()
    return cityObj.to_dict(), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def putCity(city_id):
    """Updates attributes of a City object."""
    cityObj = storage.get(City, city_id)
    if cityObj is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(cityObj, key, value)
    cityObj.save()
    return cityObj.to_dict()

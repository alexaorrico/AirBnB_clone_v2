#!/usr/bin/python3
""""Cities views"""
from flask import abort, request

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.get('/states/<state_id>/cities')
def cities_of_state(state_id):
    "Get a list of all cities of a state"
    state = storage.get(State, state_id)
    if state:
        return [city.to_dict() for city in state.cities]

    return abort(404)


@app_views.get('/cities/<id>')
def city_by_id(id):
    "Get a city by ID"
    city = storage.get(City, id)
    if city:
        return city.to_dict()

    return abort(404)


@app_views.delete('/cities/<id>')
def delete_city(id):
    "Delete the city with ID"
    city = storage.get(City, id)
    if city:
        storage.delete(city)
        storage.save()
        return {}

    return abort(404)


@app_views.post('/states/<state_id>/cities')
def create_city(state_id):
    "Create a new city"
    if not storage.get(State, state_id):
        return abort(404)
    if request.is_json:
        data = request.get_json()
        if not data.get('name'):
            return 'Missing name', 400
        new_city = City(state_id=state_id, **data)
    return 'Not a JSON', 400

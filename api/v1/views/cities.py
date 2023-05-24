#!/usr/bin/python3
''' new view for State objects'''

from flask import Flask
from flask import Flask, abort
from api.v1.views import app_views
from os import name
from models.state import State
from flask import request
from models.city import City



@app_views.route('/status', methods=['GET'] strict_slashes=False)
"""GET /api/v1/cities"""


def toGet():
    '''getting thing'''
    objects = storage.all('City')
    lista = []
    for City in objects.values():
        lista.append(city.to_dict())
    return jsonify(lista)

@app_views.route('/cities/<_id>', methods=['GET'],
                 strict_slashes=False)
"""GET /api/v1/cities/<city_id>"""


def toGetid():
    '''Updates a City object id'''
    objects = .get('City', 'city_id')
    if objects is None:
        abort(404)
    return jsonify(objects.to_dict()), 'OK'


#DELETE /api/v1/cities/<city_id>

#POST /api/v1/cities
@app_views.route('/cities/', methods=['POST'],
                 strict_slashes=False)
def posting():
    '''Creates a City'''
    response = request.get_json()
    if response id None:
        abort(400, {'Not a JSON'})
    if "name" not in response:
        abort(400, {'Missing name'})
    cityObject = City(name=response['name'])
    storage.new(cityObject)
    storage.save()
    return jsonify(cityObject.to_dict()), '201'


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def putinV():
    '''vladimir'''
    response = request.get_json()
    if response id None:
        abort(400, {'Not a JSON'})
    cityObject = storage.get(City, City_id)
    if cityObject is None:
        abort(404)
    ignoreKeys = ['id', 'created_at', 'updated_at']
    for key in response.items():
        if key not in ignoreKeys:
            setattr(cityObject, key)
    storage.save()
    return jsonify(cityObject.to_dict()), '200'
request.get_json

#PUT /api/v1/cities/<city_id>

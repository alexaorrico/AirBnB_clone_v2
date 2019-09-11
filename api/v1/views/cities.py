#!/usr/bin/python3
""" API REST for City """
from models import storage
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/cities')
@app_views.route('/cities/')
def cities_all():
    """ Route return all cities """
    return jsonify(list(map(lambda x: x.to_dict(),
                            list(storage.all(City).values()))))


@app_views.route('/cities/<id>')
def cities_id(id):
    """ Route return cities with referenced id """
    my_city = storage.get('City', id)
    try:
        return jsonify(my_city.to_dict())
    except:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_cities_id(city_id):
    """ Route delete cities with referenced id """
    my_object = storage.get('City', city_id)
    if my_object is not None:
        storage.delete(my_object)
    else:
        abort(404)
    return jsonify({}), 200

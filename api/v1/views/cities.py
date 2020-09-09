from models.base_model import BaseModel, Base
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route('states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def allcities(state_id=None):
    """ jsonify """
    lista = []
    flag = 0
    for v in storage.all(State).values():
        if v.id == state_id:
            for city in v.cities:
                lista.append(city.to_dict())
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(lista))


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def allcitiesbyid(city_id=None):
    """ jsonify """
    flag = 0
    for v in storage.all(City).values():
        if v.id == city_id:
            attr = (v.to_dict())
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(attr))


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def deletecity(city_id=None):
    if city_id is None:
        abort(404)
    dicti = {}
    flag = 0
    for v in storage.all(City).values():
        if v.id == city_id:
            storage.delete(v)
            storage.save()
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(dicti), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id=None):
    if not request.json:
        abort(400, "Not a JSON")
    if not 'name' in request.json:
        abort(400, "Missing name")
    result = request.get_json()
    print(result)
    obj = City()
    flag = 0
    for v in storage.all(State).values():
        if v.id == state_id:
            for k, v in result.items():
                flag = 1
                setattr(obj, k, v)
                setattr(obj, "state_id", state_id)
                storage.new(obj)
                storage.save()
                var = obj.to_dict()
    if flag == 0:
        abort(404)
    else:
        return (jsonify(var), 201)


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def change_city(city_id=None):
    if not request.json:
        abort(400, "Not a JSON")

    result = request.get_json()
    flag = 0
    for values in storage.all(City).values():
        if values.id == city_id:
            for k, v in result.items():
                setattr(values, k, v)
                storage.save()
                attr = (values.to_dict())
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(attr), 200)

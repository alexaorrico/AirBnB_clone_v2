#!/usr/bin/python3


"""  TODO: Doc """


from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    array_of_objs = []
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404, description="State not found")
    else:
        for value in state_obj.cities:
            array_of_objs.append(value.to_dict())
        return jsonify(array_of_objs)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_cities_ById(city_id):
    """  TODO: Doc """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404, description="State not found")
    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """  TODO: Doc """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404, description="City not found")
    try:
        storage.delete(city_obj)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(500, description="Error while deleting")


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """  TODO: Doc """
    if request.is_json:
        data = request.get_json()
        if 'name' not in data:
            abort(400, description="Missing name")
        else:
            state_obj = storage.get(State, state_id)
            if not state_obj:
                abort(404, description="State not found")
            city_obj = City(**data)  # unpack dict as key:valus
            city_obj.state_id = state_obj.id
            city_obj.save()
            return jsonify(city_obj.to_dict()), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """  TODO: Doc """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404, description="State not found")
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    bad_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key in data.keys():
        if key not in bad_keys:
            setattr(city_obj, key, data[key])
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200

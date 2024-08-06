#!/usr/bin/python3


"""  TODO: Doc """


from models.place import Place
from models.city import City
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """  TODO: Doc """
    array_of_objs = []
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404, description="City not found")
    else:
        for value in city_obj.places:
            array_of_objs.append(value.to_dict())
        return jsonify(array_of_objs)


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def get_places_ById(place_id):
    """  TODO: Doc """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404, description="State not found")
    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(place_id):
    """  TODO: Doc """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404, description="place not found")
    try:
        storage.delete(place_obj)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(500, description="Error while deleting")


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """  TODO: Doc """
    if request.is_json:
        data = request.get_json()
        if 'name' not in data:
            abort(400, description="Missing name")
        elif 'user_id':
            abort(400, description="Missing user_id")
        else:
            city_obj = storage.get(City, city_id)
            if not city_obj:
                abort(404, description="city not found")
            place_obj = Place(**data)  # unpack dict as key:valus
            place_obj.city_id = city_obj.id
            place_obj.save()
            return jsonify(place_obj.to_dict()), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_city(place_id):
    """  TODO: Doc """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404, description="Place not found")
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    bad_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key in data.keys():
        if key not in bad_keys:
            setattr(place_obj, key, data[key])
    place_obj.save()
    return jsonify(place_obj.to_dict()), 200

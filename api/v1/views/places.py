from api.v1.views import app_views
from flask import jsonify, abort, make_response,request
from flasgger.utils import swag_from
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('cities/<city_id>/places', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/place_by_city.yml', methods=['GET'])
def place_by_city(city_id):
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    place_list = []
    for city in cities.name:
        place_list.append(city.to_dict())

    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/get_place.yml', methods=['GET'])
def get_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
@swag_from('documentation/place/create_place.yml', methods=['POST'])
def create_place(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, description='Not a JSON')
    if 'user_id' not in request_data:
        abort(400, description='Missing user_id')

    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)

    if 'name' not in request_data:
        abort(400, description='Missing name')

    request_data[city_id] = city_id
    place = Place(**request_data)
    place.save()

    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/place/update_place.yml', methods=['PUT'])
def update_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, description='Not a JSON')

    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in request_data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()

    return make_response(jsonify(place.to_dict()), 200)
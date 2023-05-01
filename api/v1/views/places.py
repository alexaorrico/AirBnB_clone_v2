from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from flask import abort, jsonify, request


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    request_dict = request.get_json()
    if not request_dict:
        abort(400, 'Not a JSON')
    if 'user_id' not in request_dict:
        abort(400, 'Missing user_id')
    user = storage.get(User, request_dict['user_id'])
    if not user:
        abort(404)

    if 'name' not in request_dict:
        abort(400, 'Missing name')

    place = Place(city_id=city_id, user_id=request_dict['user_id'], name=request_dict['name'])
    for key, value in request_dict.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at', 'name']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    request_dict = request.get_json()
    if not request_dict:
        abort(400, 'Not a JSON')

    for key, value in request_dict.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

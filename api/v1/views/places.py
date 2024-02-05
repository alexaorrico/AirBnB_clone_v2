"""Module providing API endpoints for Place resources."""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieve a list of places for a specific city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieve information about a specific place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a place by its ID."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a new place for a specific city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        if 'user_id' not in data:
            return jsonify({"error": "Missing user_id"}), 400
        if 'name' not in data:
            return jsonify({"error": "Missing name"}), 400

        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)

        place = Place(**data)
        place.city_id = city_id
        storage.new(place)
        storage.save()

        return jsonify(place.to_dict()), 201
    else:
        return jsonify({"error": "Not a JSON"}), 400

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Update a place's information."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        keys_to_ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in keys_to_ignore:
                setattr(place, key, value)
        place.save()

        return jsonify(place.to_dict()), 200
    else:
        return jsonify({"error": "Not a JSON"}), 400

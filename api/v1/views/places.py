#!/usr/bin/python3
"""Place view for the web service API"""
from flask import jsonify, abort, request
from api.v1.views import app_views  # Blueprint object
from models import storage
from models.city import City
from models.place import Place
from models.user import User


# Route to get places
@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Return a JSON reponse of all place objects specified by city id
    """

    # Get list of place objects dictionary by city_id
    place_objs = [place.to_dict() for place in storage.all(
        Place).values() if place.city_id == city_id]

    if len(place_objs) == 0:
        abort(404)
    return jsonify(place_objs)

# Route to get a place object


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Return a JSON reponse of a place object specified by place id
    """

    # Get dictionary of place object by id
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


# Route to delete a city object


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete a place object specified by it id"""

    place = storage.get(Place, place_id)

    if not place:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
    return jsonify({}), 200

# Route to create a place object


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Create a new place object"""

    content = request.get_json()  # Content body
    if type(content) is not dict:
        abort(400, 'Not a Json')  # raise bad request error
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if 'user_id' not in content:
        abort(400, 'Missing user_id')  # raise bad request error
    if 'name' not in content:
        abort(400, 'Missing name')

    user = storage.get(User, content['user_id'])
    if not user:
        abort(404)
    place = Place(**content)
    place.save()

    return jsonify(place.to_dict()), 201

# Route to update a place object


@app_views.route('/place/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update a place object specified by id"""

    place = storage.get(Place, place_id)  # Get place by id

    if not place:
        abort(404)  # raise not found error

    content = request.get_json()  # Content body
    if type(content) is not dict:
        abort(400, 'Not a Json')  # raise bad request error
    for key, value in content.items():
        if key not in ['id', 'created_at', 'updated_at', 'city_id', 'user_id']:
            setattr(place, key, value)  # Update city with new data
            place.save()

    return jsonify(place.to_dict()), 200

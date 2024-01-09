#!/usr/bin/python3
"""Create a view for Place objects - handles all default RESTful API actions"""

# Import necessary modules
from flask import abort, jsonify, request
# Import the required models
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


# Route to receive all Place objects of a City
@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    '''Retrieves the list of all Place objects of a City'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


# Route for retrieving a specific Place object by ID
@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    '''Retrieves a Place object'''
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''Deletes a Place object'''
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''Creates a Place object'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''Updates a Place object'''
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            # Return 400 error if the request data is not in JSON format
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)

        place.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    '''Returns 404: Not Found'''
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''Return Bad Request message for illegal requests to the API'''
    response = {'error': 'Bad Request'}
    return jsonify(response), 400


# New endpoint: POST /api/v1/places_search
@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Retrieves Place objects based on the provided JSON search criteria"""

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []

    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]

        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)

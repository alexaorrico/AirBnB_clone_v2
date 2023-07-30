#!/usr/bin/python3
"""Place module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State
from flasgger.utils import swag_from


# GET
@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/places/get.yml', methods=['GET'])
def get_places(city_id):
    """Retrieve all Place objects in a city"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    places = [obj.to_dict() for obj in city.places]
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/places/get_id.yml', methods=['GET'])
def get_place(place_id):
    """Retrieve Place object by id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict())


# DELETE
@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/place/delete.yml', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object by id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({})


# POST
@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/places/post.yml', methods=['POST'])
def create_place(city_id):
    """Create Place object"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    kwargs = request.get_json()
    kwargs['city_id'] = city_id
    user = storage.get(User, kwargs['user_id'])

    if user is None:
        abort(404)

    obj = Place(**kwargs)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


# PUT
@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/places/put.yml', methods=['PUT'])
def update_place(place_id):
    """Update Place object"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get(Place, place_id)

    if obj is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated']:
            setattr(obj, key, value)

    storage.save()
    return jsonify(obj.to_dict())


# POST (Search)
@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/places/search.yml', methods=['POST'])
def search_places():
    """Search Place objects"""
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    resource = request.get_json()

    if resource and len(resource):
        states = resource.get('states', None)
        cities = resource.get('cities', None)
        amenities = resource.get('amenities', None)

    if not resource or not len(resource) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        all_places = []
        for place in places:
            all_places.append(place.to_dict())
        return jsonify(all_places)

    all_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            all_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in all_places:
                        all_places.append(place)

    if amenities:
        if not all_places:
            all_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        all_places = [place for place in all_places
                      if all([am in place.amenities for am in amenities_obj])]

    places = []
    for plc in all_places:
        place_dict = plc.to_dict()
        place_dict.pop('amenities', None)
        places.append(place_dict)

    return jsonify(places)

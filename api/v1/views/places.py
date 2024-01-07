#!/usr/bin/python3
""" creates a new view for places object """
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """ get list of places in a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ get place by id """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ deletes a place """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """ post method for adding a place """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    user_id = request.get_json()['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    res = request.get_json()
    place = Place(**res)
    setattr(place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ updates place based on id """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_place_search():
    """ retrieves all places """
    res = request.get_json()
    if res is None:
        abort(400, description="Not a JSON")
    if not res or (
                   not res.get('states') and
                   not res.get('cities') and
                   not res.get('amenities')):
        places = storage.all(Place)
        return jsonify([place.to_dict() for place in places.values()])

    places = []
    
    if res.get('states'):
        states = [storage.get("State", id) for id in res.get('cities')]
        for city in cities:
            for place in city.places:
                if place not in places:
                    places.append(place)

    if not places:
        places = storage.all(Place)
        places = [place for place in places.values()]

    if res.get('amenities'):
        ams = [storage.get("Amenity", id) for id in res.get('amenities')]
        i = 0
        limit = len(places)
        HBNB_API_HOST = getenv('HBNB_API_HOST')
        HBNB_API_PORT = getenv('HBNB_API_PORT')

        port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
        first_url = "http://0.0.0.0:{}/api/v1/places/".format(port)
        while i < limit:
            place = places[i]
            url = first_url + '{}/amenities'
            req = url.format(place.id)
            response = requests.get(req)
            am_d = json.loads(response.text)
            amenities = [storage.get("Amenity", o['id']) for o in am_d]
            for amenity in ams:
                if amenity not in amenities:
                    places.pop(i)
                    i -= 1
                    limit -= 1
                    break
            i += 1
    return jsonify([place.to_dict() for place in places])

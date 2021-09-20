#!/usr/bin/python3
<<<<<<< HEAD
""" Create a Index """
from api.v1.views import app_views
from flask import jsonify, abort, request
=======
"""
User for API.
"""
from api.v1.views.users import get_users
from models.city import City
from flask import abort, request, jsonify, make_response
from api.v1.views import app_views
>>>>>>> 32c217db67b8584dbcbb3f699bde8c8471d56b09
from models import storage
from models.place import Place


<<<<<<< HEAD
@app_views.route("/places", strict_slashes=False)
def get_places():
    """ return all state objects"""
    places = storage.all(Place).values()
    resultado = []

    for state in places:
        resultado.append(state.to_dict())

    return jsonify(resultado)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_states_id(state_id=None):
    """ get state for id """
    states = storage.all("State").values()
    resultado = []
    if state_id is not None:
        for state in states:
            if state_id == state.id:
                return jsonify(state.to_dict())
        return abort(404)

    return jsonify(resultado)


@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_state(state_id=None):
    """ Deletes state by id """
    try:
        state = storage.get(State, state_id)

        if state is not None:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200

        abort(404)
    except:
        abort(404)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    """ Creates new state """
    try:
        state = request.get_json()

        if state.get("name") is None:
            return jsonify({"error": "Missing name"}), 400
    except:
        return jsonify({"error": "Not a JSON"}), 400

    state = State(**state)
    storage.save()

    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_states(state_id=None):
    """ Updates state """
    try:
        json = request.get_json()

        if isinstance(json, dict) is False:
            raise Exception(400)
    except:
        return jsonify({"error": "Not a JSON"}), 400

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    att_skip = ["id", "created_at", "updated_at"]
    for key, value in json.items():
        if key not in att_skip:
            setattr(state, key, value)

    state.save()

    return jsonify(state.to_dict()), 200
=======
@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Returns all places in jason format"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    list_place = []
    for place in city.places:
        if place.city_id == city_id:
            list_place.append(place.to_dict())
    return jsonify(list_place)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_id_place(place_id):
    """Returns city_id in json format"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place"""
    place = storage.get(Place, place_id)
    if place:
        place.delete()
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates places"""
    places = request.get_json()

    if not places:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in places:
        return (jsonify({'error': 'Missing user_id'}), 400)
    if 'name' not in places:
        return (jsonify({'error': 'Missing name'}), 400)

    get_city = storage.get(City, city_id)
    if get_city is None:
        abort(404)

    get_user = storage.get("User", places['user_id'])
    if get_user is None:
        abort(404)

    new_place = Place(**places)
    storage.new(new_place)
    storage.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Updates a place """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
>>>>>>> 32c217db67b8584dbcbb3f699bde8c8471d56b09

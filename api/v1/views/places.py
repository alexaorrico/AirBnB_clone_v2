from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State


@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def get_places_by_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "name" not in data:
        abort(400, "Missing name")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    new_place = Place(city_id=city_id, **data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    try:
        request_data = request.get_json()
    except Exception as e:
        abort(400, "Not a JSON")

    states = request_data.get("states", [])
    cities = request_data.get("cities", [])
    amenities = request_data.get("amenities", [])

    places_result = set()

    if not states and not cities and not amenities:
        # Retrieve all Place objects if no filters provided
        places_result = storage.all(Place).values()
    else:
        # Filter based on states and cities
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                places_result.update(state.places)
                cities += [city.id for city in state.cities]

        # Filter based on cities
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places_result.update(city.places)

        # Filter based on amenities
        if amenities:
            amenities_set = set(amenities)
            places_result = [
                place
                for place in places_result
                if amenities_set.issubset(set(place.amenities))
            ]

    return jsonify([place.to_dict() for place in places_result])

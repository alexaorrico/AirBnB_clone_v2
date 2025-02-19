#!/usr/bin/python3
""" Python script for State Routes & views"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"])
def get_places(city_id):
    """ Get methods for amenitites routes"""
    # get method
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    if request.method == "GET":
        places = []
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)

    # post method
    elif request.method == "POST":
        try:
            data = request.get_json(force=True)
        except Exception:
            return jsonify({'error': 'Not a JSON'}), 400
        if not data:
            return jsonify({'error': 'Not a JSON'}), 400
        user_id = data.get("user_id")
        if user_id is None:
            return "Missing user_id", 400
        user = storage.get("User", user_id)
        if user is None:
            abort(404)
        if "name" not in data:
            return jsonify({'error': 'Missing name'}), 400
        data["city_id"] = city_id
        # create new place
        place = Place(**data)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"])
def get_place_id(place_id):
    """ Get methods for retriving places objects by id"""
    place = storage.get("Place", place_id)
    if place is None:
        return jsonify({'error': 'place not found'}), 404
    # return jsonify(place.to_dict())

    # DELETE method
    if request.method == "DELETE":
        place.delete()
        storage.save()
        return jsonify({}), 200

    # GET method
    elif request.method == "GET":
        return jsonify(place.to_dict())

    # PUT method
    elif request.method == "PUT":
        try:
            data = request.get_json(force=True)
        except Exception:
            return jsonify({'error': 'Not a JSON'}), 400

        if not data:
            return jsonify({'error': 'Not a JSON'}), 400
        keys_ignored = {"id", "created_at", "user_id", "city_id", "updated_at"}
        [setattr(place, k, v) for k, v in data.items()
         if k not in keys_ignored]
        place.save()
        return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"])
def search_place():
    """Retrieves all Place objects based on search criteria."""
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    places = []
    place_ids = set()

    if not data:
        places = [place.to_dict() for place in storage.all("Place").values()]
        return jsonify(places)

    # Get places by state
    if "states" in data:
        for state_id in data["states"]:
            state = storage.get("State", state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        if place.id not in place_ids:
                            places.append(place.to_dict())
                            place_ids.add(place.id)

    # Get places by city
    if "cities" in data:
        for city_id in data["cities"]:
            city = storage.get("City", city_id)
            if city:
                for place in city.places:
                    if place.id not in place_ids:
                        places.append(place.to_dict())
                        place_ids.add(place.id)

    # Filter places by amenities
    if data.get("amenities"):
        # Create a set of amenity IDs instead of objects
        amenities_set = set(data["amenities"])  # Set of required amenity IDs

        if places:
            x = 0
            for place in places:
                if x < 8:
                    a_id = [amenity['id'] for amenity in place['amenities']]
                    print(place)
                    print()
                    print(a_id)
                    print()
                x += 1

            places = [place for place in places if amenities_set.issubset([
                amenity['id'] for amenity in place['amenities']])]

        # If state and city weren't selected,
        # fetch all places and filter by amenity IDs
        else:
            places = [place for place in storage.all("Place").values()
                      if amenities_set.issubset({amenity.id for amenity
                                                in place.amenities})]

            places = [place.to_dict() for place in places]

    return jsonify(places)


'''
@app_views.route("/places_search", methods=["POST"])
def search_place():
    """retrieves all Place objects depending
    of the JSON in the body of the request."""
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    places = []
    if data.get("states"):
        for state_id in data.get("states"):
            state = storage.get("State", state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        places.append(place.to_dict())
    if data.get("cities"):
        for city_id in data.get("cities"):
            city = storage.get("City", city_id)
            if city:
                for place in city.places:
                    if place not in places:
                        places.append(place.to_dict())
    if data.get("amenities"):
        for amenity_id in data.get("amenities"):
            amenity = storage.get("Amenity", amenity_id)
            if amenity:
                for place in places:
                    if amenity not in place.amenities:
                        places.remove(place)

    return jsonify(places)
    '''

'''
#revise the below code expecially the use of sets
@app_views.route("/places_search", methods=["POST"])
def search_place():
    """Retrieves all Place objects depending on the
    JSON in the body of the request."""
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    places = set()  # Use a set to avoid duplicates

    # Retrieve places based on states
    if data.get("states"):
        for state_id in data.get("states"):
            state = storage.get("State", state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        places.add(place)

    # Retrieve places based on cities
    if data.get("cities"):
        for city_id in data.get("cities"):
            city = storage.get("City", city_id)
            if city:
                for place in city.places:
                    places.add(place)

    # Convert set to list for easier manipulation
    places = list(places)

    # Filter places based on amenities
    if data.get("amenities"):
        amenity_ids = set(data.get("amenities"))
        # Use a set for faster lookups
        filtered_places = []
        for place in places:
            place_amenity_ids = {amenity.id for amenity in place.amenities}
            if amenity_ids.issubset(place_amenity_ids):
                filtered_places.append(place)
        places = filtered_places

    # Convert places to dictionaries
    return jsonify([place.to_dict() for place in places])

'''

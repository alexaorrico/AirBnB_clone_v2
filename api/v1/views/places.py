#!/usr/bin/python3
'''
The following script creates a Place objects view
and handles all default RESTful API actions
'''


# Importing necessary modules
from flask import abort, jsonify, request
# Import the required models
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


# Retrieving all Place objects of a City
@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    '''
    The method retrieves the list of all Place objects of a City

    Args:
        city_id (str): The ID of the City.

    Returns:
        JSON: List of dictionaries representing Place objects.
    '''
    # Getting the City object with the given ID from the storage
    city = storage.get(City, city_id)
    if not city:
        # Returning 404 error if the City object is not found
        abort(404)

    # Getting all Place objects of the City and convert them to dictionaries
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


# Retrieving a specific Place object by ID
@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    '''
    This method retrieves a Place object

    Args:
        place_id (str): The ID of the Place.

    Returns:
        JSON: Dictionary representing the Place object.
    '''
    # Getting the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if place:
        # Returning the Place object in JSON format
        return jsonify(place.to_dict())
    else:
        # Returning 404 error if the Place object is not found
        abort(404)


# Deleting a specific Place object by ID
@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''
    This method deletes a Place object

    Args:
        place_id (str): The ID of the Place.

    Returns:
        JSON: Empty dictionary with 200 status code.
    '''
    # Getting the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if place:
        # Deleting the Place object from the storage and save changes
        storage.delete(place)
        storage.save()
        # Returning an empty JSON with 200 status code
        return jsonify({}), 200
    else:
        # Returning 404 error if the Place object is not found
        abort(404)


# Creating a new Place object
@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''
    This method creates a Place object

    Args:
        city_id (str): The ID of the City.

    Returns:
        JSON: Dictionary representing the newly created Place object.
    '''
    # Getting the City object with the given ID from the storage
    city = storage.get(City, city_id)
    if not city:
        # Returning 404 error if the City object is not found
        abort(404)

    # Checking if the request data is in JSON format
    if not request.get_json():
        # Returning 400 error if the request data is not in JSON format
        abort(400, 'Not a JSON')

    # Getting the JSON data from the request
    data = request.get_json()
    if 'user_id' not in data:
        # Returning 400 error if 'user_id' key is missing in the JSON data
        abort(400, 'Missing user_id')
    if 'name' not in data:
        # Returning 400 error if 'name' key is missing in the JSON data
        abort(400, 'Missing name')

    # Getting the User object with the given user_id from the storage
    user = storage.get(User, data['user_id'])
    if not user:
        # Returning 404 error if the User object is not found
        abort(404)

    # Assigning the city_id to the JSON data
    data['city_id'] = city_id
    # Creating a new Place object with the JSON data
    place = Place(**data)
    # Saving the Place object to the storage
    place.save()
    # Returning the newly created Place object in JSON format with 201 status
    return jsonify(place.to_dict()), 201


# Updating an existing Place object by ID
@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''
    This method updates a Place object

    Args:
        place_id (str): The ID of the Place.

    Returns:
        JSON: Dictionary representing the updated Place object.
    '''
    # Getting the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if place:
        # Checking if the request data is in JSON format
        if not request.get_json():
            # Returning 400 error if the request data is not in JSON format
            abort(400, 'Not a JSON')

        # Getting the JSON data from the request
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        # Updating the attributes of the Place object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)

        # Saving the updated Place object to the storage
        place.save()
        # Returning the updated Place object in JSON format with code200
        return jsonify(place.to_dict()), 200
    else:
        # Returning 404 error if the Place object is not found
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    '''
    This method returns 404: Not Found

    Args:
        error (Exception): The exception object.

    Returns:
        JSON: Dictionary with 'error' key and 'Not found' value.
    '''
    # Return a JSON response for 404 error
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''
    This method returns Bad Request message for illegal requests to the API

    Args:
        error (Exception): The exception object.

    Returns:
        JSON: Dictionary with 'error' key and 'Bad Request' value.
    '''
    # Return a JSON response for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400


# New endpoint: POST /api/v1/places_search
@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves Place objects based on the provided JSON search criteria

    Returns:
        JSON: List of dictionaries representing Place objects.
    """
    # Check if the request contains valid JSON
    if request.get_json() is None:
        abort(400, description="Not a JSON")
    # Extract data from the JSON request body
    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    # If no criteria provided, retrieve all places
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

    # Filter and retrieve places based on states criteria
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    # Filtering and retrieving places based on cities criteria
    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    # Filter places based on amenities criteria
    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]

        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    # Prepare the final list of places for response
    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    # Return the list of places in JSON format
    return jsonify(places)

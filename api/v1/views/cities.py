#!/usr/bin/python3
'''
Create a new view for City objects - handles all default RESTful API actions.
'''

# Import necessary modules
from flask import abort, jsonify, request
# Import the State and City models
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage


# Route for retrieving all City objects of a specific State
@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    '''
    Retrieves the list of all City objects of a State.
    '''
    # Get the State object with the given ID from the storage
    state = storage.get(State, state_id)
    if not state:
        # Return 404 error if the State object is not found
        abort(404)

    # Get all City objects associated with
    #   the State and convert them to dictionaries
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


# Route for retrieving a specific City object by ID
@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    '''
    Retrieves a City object.
    '''
    # Get the City object with the given ID from the storage
    city = storage.get(City, city_id)
    if city:
        # Return the City object in JSON format
        return jsonify(city.to_dict())
    else:
        # Return 404 error if the City object is not found
        abort(404)


# Route for deleting a specific City object by ID
@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''
    Deletes a City object.
    '''
    # Get the City object with the given ID from the storage
    city = storage.get(City, city_id)
    if city:
        # Delete the City object from the storage and save changes
        storage.delete(city)
        storage.save()
        # Return an empty JSON with 200 status code
        return jsonify({}), 200
    else:
        # Return 404 error if the City object is not found
        abort(404)


# Route for creating a new City object under a specific State
@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    '''
    Creates a City object.
    '''
    # Get the State object with the given ID from the storage
    state = storage.get(State, state_id)
    if not state:
        # Return 404 error if the State object is not found
        abort(404)

    # Check if the request data is in JSON format
    if not request.get_json():
        # Return 400 error if the request data is not in JSON format
        abort(400, 'Not a JSON')

    # Get the JSON data from the request
    data = request.get_json()
    if 'name' not in data:
        # Return 400 error if 'name' key is missing in the JSON data
        abort(400, 'Missing name')

    # Assign the 'state_id' key in the JSON data
    data['state_id'] = state_id
    # Create a new City object with the JSON data
    city = City(**data)
    # Save the City object to the storage
    city.save()
    # Return the newly created City object in JSON format with 201 status code
    return jsonify(city.to_dict()), 201


# Route for updating an existing City object by ID
@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''
    Updates a City object.
    '''
    # Get the City object with the given ID from the storage
    city = storage.get(City, city_id)
    if city:
        # Check if the request data is in JSON format
        if not request.get_json():
            # Return 400 error if the request data is not in JSON format
            abort(400, 'Not a JSON')

        # Get the JSON data from the request
        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        # Update the attributes of the City object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)

        # Save the updated City object to the storage
        city.save()
        # Return the updated City object in JSON format with 200 status code
        return jsonify(city.to_dict()), 200
    else:
        # Return 404 error if the City object is not found
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    '''
    404: Not Found.
    '''
    # Return a JSON response for 404 error
    return jsonify({'error': 'Not found'}), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''
    Return Bad Request message for illegal requests to API.
    '''
    # Return a JSON response for 400 error
    return jsonify({'error': 'Bad Request'}), 400

#!/usr/bin/python3
'''
The following script creates an Amenity objects view
and handles all default RESTful API actions
'''

# Importing the necessary modules
from flask import abort, jsonify, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


# Retrieving all Amenity objects
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    '''
    This method retrieves the list of all Amenity objects.

    Returns:
        JSON: List of all Amenity objects in JSON format.
    '''
    # Get all Amenity objects from the storage
    amenities = storage.all(Amenity).values()
    # Convert objects to dictionaries and jsonify the list
    return jsonify([amenity.to_dict() for amenity in amenities])


# Retrieving a specific Amenity object by ID
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    '''This method retrieves an Amenity object'''
    # Getting the Amenity object with the given ID from the storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Returning the Amenity object in JSON format
        return jsonify(amenity.to_dict())
    else:
        # Returning 404 error if the Amenity object is not found
        abort(404)


# Deleting a specific Amenity object by ID
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    The following method deletes an Amenity object by ID.

    Args:
        amenity_id (str): The ID of the Amenity object.

    Returns:
        JSON: Empty JSON with a status code of 200.
    Raises:
        404: If the Amenity object with the given ID is not found.
    """
    # Getting the Amenity object with the given ID from the storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Deleting the Amenity object from the storage and save changes
        storage.delete(amenity)
        storage.save()
        # Returning an empty JSON with 200 status code
        return jsonify({}), 200
    else:
        # Returning 404 error if the Amenity object is not found
        abort(404)


# Creating a new Amenity object
@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    This method creates an Amenity object.

    Returns:
        JSON: Newly created Amenity object in JSON format
        with a status code of 201.
    Raises:
        400: If the request data is not in JSON format
        or if the 'name' key is missing.
    """
    if not request.get_json():
        # Returning 400 error if the request data is not in JSON format
        abort(400, 'Not a JSON')

    # Getting the JSON data from the request
    data = request.get_json()
    if 'name' not in data:
        # Returning 400 error if 'name' key is missing in the JSON data
        abort(400, 'Missing name')

    # Creating a new Amenity object with the JSON data
    amenity = Amenity(**data)
    # Saving the Amenity object to the storage
    amenity.save()
    # Returning the newly created Amenity
    # object in JSON format with 201 status code
    return jsonify(amenity.to_dict()), 201


# Updating an existing Amenity object by ID
@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    This method updates an Amenity object by ID.

    Args:
        amenity_id (str): The ID of the Amenity object.

    Returns:
        JSON: Updated Amenity object in JSON format with a status code of 200
    Raises:
        400: If the request data is not in JSON format.
        404: If the Amenity object with the given ID is not found.
    """
    # Getting the Amenity object with the given ID from the storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Returning 400 error if the request data is not in JSON format
        if not request.get_json():
            abort(400, 'Not a JSON')

        # Getting the JSON data from the request
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        # Updating the attributes of the Amenity object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)

        # Saving the updated Amenity object to the storage
        amenity.save()
        # Returning the updated Amenity object in JSON format with code200
        return jsonify(amenity.to_dict()), 200
    else:
        # Returning 404 error if the Amenity object is not found
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    """This method returns:
        JSON: Error response for 404 status code.
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """
    The method returns Bad Request message for illegal requests to the API
    Returns:
        JSON: Error response for 400 status code.
    """
    # Returning a JSON response for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400

#!/usr/bin/python3
'''
The following script creates a new Review objects view
and handles all default RESTful API
'''


# Importing necessary modules
from flask import abort, jsonify, request
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from models import storage


# Retrieving all Review objects of a Place
@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    '''
    This method retrieves the list of all Review objects of a Place

    Args:
        place_id (str): The ID of the Place.

    Returns:
        JSON: List of dictionaries representing Review objects.
    '''
    # Getting the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if not place:
        # Returning  404 error if the Place object is not found
        abort(404)

    # Getting all Review objects of the Place and convert them to dictionaries
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


# Retrieving a specific Review object by ID
@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    '''
    This method retrieves a Review object

    Args:
        review_id (str): The ID of the Review.

    Returns:
        JSON: Dictionary representing the Review object.
    '''
    # Getting the Review object with the given ID from the storage
    review = storage.get(Review, review_id)
    if review:
        # Returning the Review object in JSON format
        return jsonify(review.to_dict())
    else:
        # Returning 404 error if the Review object is not found
        abort(404)


# Deleting a specific Review object by ID
@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    '''
    This method deletes a Review object

    Args:
        review_id (str): The ID of the Review.

    Returns:
        JSON: Empty dictionary with 200 status code.
    '''
    # Getting the Review object with the given ID from the storage
    review = storage.get(Review, review_id)
    if review:
        # Deleting the Review object from the storage and save changes
        storage.delete(review)
        storage.save()
        # Returning an empty JSON with 200 status code
        return jsonify({}), 200
    else:
        # Returning 404 error if the Review object is not found
        abort(404)


# Creating a new Review object
@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''
    This method creates a Review object

    Args:
        place_id (str): The ID of the Place.

    Returns:
        JSON: Dictionary representing the newly created Review object.
    '''
    # Getting the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if not place:
        # Returning 404 error if the Place object is not found
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
    if 'text' not in data:
        # Returning 400 error if 'text' key is missing in the JSON data
        abort(400, 'Missing text')

    # Getting the User object with the given user_id from the storage
    user = storage.get(User, data['user_id'])
    if not user:
        # Returning 404 error if the User object is not found
        abort(404)

    # Assigning the place_id to the JSON data
    data['place_id'] = place_id
    # Creating a new Review object with the JSON data
    review = Review(**data)
    # Saving the Review object to the storage
    review.save()
    # Returning the newly created Review object in JSON format with 201 status
    return jsonify(review.to_dict()), 201


# Updating an existing Review object by ID
@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''
    This method updates a Review object

    Args:
        review_id (str): The ID of the Review.

    Returns:
        JSON: Dictionary representing the updated Review object.
    '''
    # Getting the Review object with the given ID from the storage
    review = storage.get(Review, review_id)
    if review:
        # Checking if the request data is in JSON format
        if not request.get_json():
            # Returning 400 error if the request data is not in JSON format
            abort(400, 'Not a JSON')

        # Getingt the JSON data from the request
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        # Updating the attributes of the Review object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)

        # Saving the updated Review object to the storage
        review.save()
        # Returning the updated Review obj in JSON format with 200 status code
        return jsonify(review.to_dict()), 200
    else:
        # Returning 404 error if the Review object is not found
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    '''
    This method returns 404: Not Found


    Returns:
        JSON: Error message for 404 status code.
    '''
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''
    This method returns Bad Request message for illegal requests to the API

    Returns:
        JSON: Error message for 400 status code.
    '''
    response = {'error': 'Bad Request'}
    return jsonify(response), 400

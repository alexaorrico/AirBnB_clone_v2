#!/usr/bin/python3
'''
Create a new view for Review objects - handles all default RESTful API
'''

# Import necessary modules
from flask import abort, jsonify, request
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from models import storage


# Route for retrieving all Review objects of a Place
@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    '''
    Retrieves the list of all Review objects of a Place
    '''
    # Get the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if not place:
        # Return 404 error if the Place object is not found
        abort(404)

    # Get all Review objects of the Place and convert them to dictionaries
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


# Route for retrieving a specific Review object by ID
@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    '''
    Retrieves a Review object
    '''
    # Get the Review object with the given ID from the storage
    review = storage.get(Review, review_id)
    if review:
        # Return the Review object in JSON format
        return jsonify(review.to_dict())
    else:
        # Return 404 error if the Review object is not found
        abort(404)


# Route for deleting a specific Review object by ID
@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    '''
    Deletes a Review object
    '''
    # Get the Review object with the given ID from the storage
    review = storage.get(Review, review_id)
    if review:
        # Delete the Review object from the storage and save changes
        storage.delete(review)
        storage.save()
        # Return an empty JSON with 200 status code
        return jsonify({}), 200
    else:
        # Return 404 error if the Review object is not found
        abort(404)


# Route for creating a new Review object
@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''
    Creates a Review object
    '''
    # Get the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if not place:
        # Return 404 error if the Place object is not found
        abort(404)

    # Check if the request data is in JSON format
    if not request.get_json():
        # Return 400 error if the request data is not in JSON format
        abort(400, 'Not a JSON')

    # Get the JSON data from the request
    data = request.get_json()
    if 'user_id' not in data:
        # Return 400 error if 'user_id' key is missing in the JSON data
        abort(400, 'Missing user_id')
    if 'text' not in data:
        # Return 400 error if 'text' key is missing in the JSON data
        abort(400, 'Missing text')

    # Get the User object with the given user_id from the storage
    user = storage.get(User, data['user_id'])
    if not user:
        # Return 404 error if the User object is not found
        abort(404)

    # Assign the place_id to the JSON data
    data['place_id'] = place_id
    # Create a new Review object with the JSON data
    review = Review(**data)
    # Save the Review object to the storage
    review.save()
    # Return the newly created Review object in JSON format with 201 status
    return jsonify(review.to_dict()), 201


# Route for updating an existing Review object by ID
@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''
    Updates a Review object
    '''
    # Get the Review object with the given ID from the storage
    review = storage.get(Review, review_id)
    if review:
        # Check if the request data is in JSON format
        if not request.get_json():
            # Return 400 error if the request data is not in JSON format
            abort(400, 'Not a JSON')

        # Get the JSON data from the request
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        # Update the attributes of the Review object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)

        # Save the updated Review object to the storage
        review.save()
        # Return the updated Review object in JSON format with 200 status code
        return jsonify(review.to_dict()), 200
    else:
        # Return 404 error if the Review object is not found
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    '''
    Returns 404: Not Found
    '''
    # Return a JSON response for 404 error
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''
    Return Bad Request message for illegal requests to the API
    '''
    # Return a JSON response for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400

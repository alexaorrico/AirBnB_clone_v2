#!/usr/bin/python3
'''Contains the states view for the API.'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a new review object """
    # grab the place object from storage
    place = storage.get(Place, place_id)

    if place is None:  # if place_id isnt found in storage
        abort(404)

    # if body doesn't contain valid JSON
    if not request.is_json:
        abort(400, "Not a JSON")

    # else transform HTTP body into a dict
    body = request.get_json()

    # if the text key doesnt exist in the body dict
    if body.get("text") is None:
        abort(400, "Missing text")

    # if the user_id key doesnt exist in the body dict
    user_id = body.get("user_id")
    if user_id is None:
        abort(400, "Missing user_id")

    # check using user_id to see if user exists in storage
    if storage.get(User, user_id) is None:  # user_id not found in storage
        abort(404)

    # create and save the new review instance
    new_review = Review(**body)
    new_review.place_id = place_id
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def retrieve_reviews(place_id):
    """ Retrieves a list of all Review objects of a Place """
    # grab the place object from storage
    place = storage.get(Place, place_id)

    if place is None:  # if place_id isnt found in storage
        abort(404)

    # convert all review objects into dictionaries & put in list
    review_list = [review.to_dict() for review in place.reviews]

    # return the list of reviews
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def retrieve_review(review_id):
    """ Retrieves a single review object based on its review_id """
    # grab the review object from storage
    review = storage.get(Review, review_id)

    if review:  # return the jsonified object
        return jsonify(review.to_dict())
    else:  # else if review is None
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates specific instance of a review object """
    # retrieve the object by review_id if it exists
    review = storage.get(Review, review_id)

    # abort if review with specific review_id can't be found
    if review is None:
        abort(404)

    # if body doesn't contain valid JSON
    if not request.is_json:
        abort(400, "Not a JSON")

    # else transform HTTP body into a dict
    body = request.get_json()

    # ignore id, created_at, updated_at keys during update
    excluded_keys = ["id", "user_id", "place_id" "created_at", "updated_at"]

    # iterate over body dict & update the review object
    # with the new values from body dict
    for key, value in body.items():
        if key not in excluded_keys:
            setattr(review, key, value)

    # save the updated review instance
    storage.save()

    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes specific instance of an review object """
    # retrieve the object by review_id if it exists
    review = storage.get(Review, review_id)

    # delete the object if it exists
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:  # else if review is None
        abort(404)

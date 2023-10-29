#!/usr/bin/python3
""" Module containing Review View """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ Retrieves the list of all Review objects associated with a Place
        object.

    Args:
        place_id (str): The UUID4 string representing a Place object.

    Returns:
        List of dictionaries representing Review objects in JSON format.
        404 error if `place_id` is not linked to any Place object.
    """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    reviews = [review.to_dict() for review in place_obj.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Retrieves a Review object based on `review_id`.

    Args:
        review_id (str): The UUID4 string representing a review object.

    Returns:
        Dictionary represention of a Review object in JSON format.
        404 error if `review_id` is not linked to any Review object.
    """
    review_obj = storage.get("Review", review_id)
    if review_obj is None:
        abort(404)
    return jsonify(review_obj.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object based on `review_id`.

    Args:
        review_id (str): The UUID4 string representing a Review object.

    Returns:
        Returns an empty dictionary with the status code 200.
        404 error if `review_id` is not linked to any Review object.
    """
    review_obj = storage.get("Review", review_id)
    if review_obj is None:
        abort(404)
    review_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def add_review(place_id):
    """ Creates a Review object to associate to a Place object with the HTTP
        body request fields as the values to set the Review object with.

    Args:
        place_id (str): The UUID4 string representing a Place object the new
        Review object will be associated to.

    Returns:
        Returns the new Review object as a  dictionary in JSON format
        with the status code 201.
        400 error if HTTP body request is not a valid JSON or if the dictionary
        passed does not contain the key `email` and/or `password`.
        404 error if `place_id` is not linked to any Place object.
    """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    u_id = fields.get('user_id')
    if u_id is None:
        return "Missing user_id", 400
    if storage.get("User", u_id) is None:
        abort(404)
    if fields.get('text') is None:
        return "Missing text", 400
    fields["place_id"] = place_id
    new_review = Review(**fields)
    new_review.save()
    """ May need to call `get` on new_user for all attributes to show """
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def edit_review(review_id):
    """ Edit a Review object using `review_id` and HTTP body request fields.

    Args:
        review_id (str): The UUID4 string representing a Review object.

    Returns:
        Returns the Review object as a dictionary in JSON format with the
        status code 200.
        400 error if the HTTP body request is not a valid JSON.
        404 error if `review_id` is not linked to a Reivew object.
    """
    review_obj = storage.get("Review", review_id)
    if review_obj is None:
        abort(404)
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    for key in fields:
        if key in ['id', 'user_id', 'place_id', 'created_at', 'update_at']:
            continue
        if hasattr(review_obj, key):
            setattr(review_obj, key, fields[key])
    review_obj.save()
    return jsonify(review_obj.to_dict()), 200

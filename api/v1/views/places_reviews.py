#!/usr/bin/python3
"""
Reviews
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews(place_id):
    """
    Retrieves the list of all Reviews objects of the Place
    """
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    reviews_list = []
    for review in places.reviews:
        reviews_list.append(review.to_dict())
    return(jsonify(reviews_list))


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def reviews_id(review_id):
    """
    Retrieves a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return (jsonify(review.to_dict()))


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        error = {"error": "Not a JSON"}
        return (jsonify(error), 400)
    if "user_id" not in request.get_json():
        no_user_id = {"error": "Missing user_id"}
        return (jsonify(no_user_id), 400)
    obj_dict = request.get_json()
    user = storage.get(User, obj_dict['user_id'])
    if user is None:
        abort(404)
    if "text" not in request.get_json():
        no_text = {"error": "Missing text"}
        return (jsonify(no_text), 400)
    obj_dict['place_id'] = place.id
    review = Review(**obj_dict)
    review.save()
    return (jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        error = {"error": "Not a JSON"}
        return (jsonify(error), 400)
    obj_dict = request.get_json()
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at',
                   'updated_at']
    for key in obj_dict.keys():
        if key not in ignore_keys:
            setattr(review, key, obj_dict[key])
    review.save()
    return (jsonify(review.to_dict()), 200)

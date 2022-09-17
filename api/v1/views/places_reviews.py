#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_get(place_id):
    """Retrieves the list of all Reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)

    reviews_list = []
    all_reviews = storage.all(Review)
    for key, value in all_reviews.items():
        reviews_list.append(value.to_dict())
    return jsonify(reviews_list)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def reviews_post(place_id):
    """Creates a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)

    transform_dict = request.get_json()
    if transform_dict is None:
        abort(400, "Not a JSON")
    if 'user_id' not in transform_dict.keys():
        abort(400, "Missing user_id")

    user_id = storage.get(User, transform_dict['user_id'])
    if user_id is None:
        return abort(404)
    if 'text' not in transform_dict.keys():
        abort(400, "Missing text")
    else:
        transform_dict['place_id'] = place_id
        new_review = Review(**transform_dict)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_id_get(review_id):
    """Retrieves a Place object and 404 if it's an error"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_id_delete(review_id):
    """Deletes a Place object and 404 if it's an error"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_id_put(review_id):
    """Updates a Place object"""
    ignore_list = ['id', 'created_at', 'user_id', 'city_id', 'updated_at']
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    transform_dict = request.get_json()
    if transform_dict is None:
        abort(400, "Not a JSON")
    for key, value in transform_dict.items():
        if key not in ignore_list:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200

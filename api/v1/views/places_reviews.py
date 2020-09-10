#!/usr/bin/python3
""" New module for a view to Reviews objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.base_model import BaseModel
from models.state import State
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves all the City objects linked to a state_id """
    place = storage.get(Place, place_id)
    list_reviews = []
    if place is None:
        abort(404)
    for review in place.reviews:
        list_reviews.append(review.to_dict())
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Retrieves a review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    empty_dict = {}
    review.delete()
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a Review object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    my_dict = request.get_json()
    if my_dict is None:
        abort(400, "Not a JSON")
    if "user_id" not in my_dict:
        abort(400, "Missing user_id")
    user = storage.get(User, my_dict["user_id"])
    if user is None:
        abort(404)
    if "text" not in my_dict:
        abort(400, "Missing text")
    my_dict["place_id"] = place_id
    new_review = Review(**my_dict)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update a Review object"""
    if review_id:
        my_dict = request.get_json()
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        if my_dict is None:
            abort(400, "Not a JSON")
        for key, value in my_dict.items():
            if key not in ["id", "created_at",
                           "updated_at", "user_id",
                           "place_id"]:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200

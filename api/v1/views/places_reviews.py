#!/usr/bin/python3
""" Handles all default RESTFul API actions for Review object """
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_review_by_placeiD(place_id=None):
    """Get the reviews for a place"""
    reviews = []
    place = storage.get(Place, place_id)
    if place:
        for place in place.reviews:
            reviews.append(place.to_dict())
        return jsonify(reviews)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review_by_reviewiD(review_id=None):
    """ Retrieves a review with his iD """
    rev = storage.get(Review, review_id)
    if rev:
        return jsonify(rev.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id=None):
    """ Delete a review"""
    if review_id:
        review = storage.get(Review, review_id)
        if review:
            storage.delete(review)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id=None):
    """ Creates review for a given place """
    review_dict = request.get_json()

    if not review_dict:
        abort(400, "Not a JSON")
    if 'text' not in review_dict:
        abort(400, "Missing text")
    if 'user_id' not in review_dict:
        abort(400, "Missing user_id")

    place = storage.get(Place, place_id)
    user = storage.get(User, review_dict["user_id"])
    if user and place:
        new_review = Review(**review_dict)
        new_review.place_id = place.id
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def put_review(review_id=None):
    """update a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    requeste = request.get_json()
    if requeste is None:
        abort(400, "Not a JSON")

    for key, value in requeste.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200

#!/usr/bin/python3
"""Place review file"""

from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET\
'], strict_slashes=False)
def displayReviewsByPlace(place_id):
    """Return the reviews by place if not error 404
    """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    list = []
    for i in place.reviews:
        list.append(i.to_dict())
    return jsonify(list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def displayReviewbyId(review_id):
    """Return the review by id if not error 404"""
    reviews = storage.get('Review', review_id)
    if not reviews:
        abort(404)
    return jsonify(reviews.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE\
'], strict_slashes=False)
def deleteReview(review_id):
    """Delete a review if not error 404"""
    reviews = storage.get('Review', review_id)
    if not reviews:
        abort(404)
    storage.delete(reviews)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST\
'], strict_slashes=False)
def createReview(place_id):
    """Create a review for a place if not error 404"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    review = request.get_json()
    if not review:
        abort(400, {'Not a JSON'})
    if 'user_id' not in review.keys():
        abort(400, {'Missing user_id'})
    userid = storage.get('User', review['user_id'])
    if not userid:
        abort(404)
    if 'text' not in review.keys():
        abort(400, {'Missing text'})
    new_review = Review(**review)
    new_review.place_id = place_id
    storage.new(new_review)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def updateReview(review_id):
    """Update a review if not error 404"""
    rev = storage.get('Review', review_id)
    if not rev:
        abort(404)
    review = request.get_json()
    if not review:
        abort(400, {'Not a JSON'})

    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in review.items():
        if key not in ignore:
            setattr(rev, key, value)
    storage.save()
    return make_response(jsonify(rev.to_dict()), 200)

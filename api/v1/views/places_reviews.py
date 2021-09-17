#!/usr/bin/python3
""" Handles all default RESTFul API actions for Review object """
import re
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review


@app_views.route('/place/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_review_by_placeiD(place_id):
    """Get the reviews for a place"""
    reviews = []
    place = storage.all('Place', place_id).values() 
    if place: 
        for review in place.review:
            reviews.append(place.to_dict())
        return jsonify(reviews)
    else:
        abort(404)


@app_views.route('/review/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_by_reviewiD(review_id=None):
    """ Retrieves a review with his iD """
    rev  = storage.all('Review', review_id).values() 
    if rev: 
        return jsonify(rev.to_dict())
    else:
        abort(404)

@app_views.route('/review/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id=None):
    """ Delete a review"""
    if review_id is None:
        abort(404)
    review = storage.get("Review", review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/review/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """ Creates review for a given place """
    review_dict = request.get_json()
    place = storage.get('Place', place_id)
    if not review_dict:
        abort (400, "Not a JSON")
    elif 'text' not in review_dict.keys():
        abort (400, "Missing text")
    elif 'user_id' not in review_dict.keys():
        abort (400, "Missing user_id")
    elif storage.get('User', request.get_json()['user_id']) and place:
        review = Review(**review_dict)
        review.place_id = place_id
        review.save()
        return (jsonify(review.to_dict()), 201)
    abort(404)

@app_views.route('/review/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """update a review"""
    state = storage.get("State", review_id)
    if state is None:
        abort(404)
    requeste = request.get_json()
    if requeste is None:
        abort(400, "Not a JSON")
    for key, value in requeste.items():
        setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200

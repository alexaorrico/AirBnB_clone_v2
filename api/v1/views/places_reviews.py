#!/usr/bin/python3
"""Review view module"""
from models import storage
from models.review import Review
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def places_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    if storage.get('Place', place_id) is None:
        abort(404)
    reviews_place = []
    reviews_objs = storage.all('Review')
    for key, value in reviews_objs.items():
        if place_id == value.place_id:
            reviews_place.append(value.to_dict())
    return jsonify(reviews_place), 201


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review(review_id):
    """Retrieves a Review object"""
    new_review = storage.get('Review', review_id)
    if new_review is None:
        abort(404)
    return jsonify(new_review.to_dict())

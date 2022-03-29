#!/usr/bin/python3
""" Views for Reviews """


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def review_by_place_id(place_id):
    """ Return all reviews of a place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    reviews_list = []
    for review in reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/places/<place_id>/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review_by_id(place_id, review_id):
    """ Return a review """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_reviews_by_id(review_id):
    """ Delete a review """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """ Create a review """
    if not request.json:
        abort(400, 'Not a JSON')
    if 'title' not in request.json:
        abort(400, 'Missing title')
    if 'text' not in request.json:
        abort(400, 'Missing text')
    if 'rating' not in request.json:
        abort(400, 'Missing rating')
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    review = Review(**request.json)
    review.place_id = place.id
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Update a review """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'title' in request.json:
        review.title = request.json['title']
    if 'text' in request.json:
        review.text = request.json['text']
    if 'rating' in request.json:
        review.rating = request.json['rating']
    storage.save()
    return jsonify(review.to_dict()), 200

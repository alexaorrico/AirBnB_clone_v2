#!/usr/bin/python3
"""places routes"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.review import Review


@app_views.route('/places/<string:place_id>/reviews', strict_slashes=False)
def place_reviews(place_id):
    """list all reviews by place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404, 'Not found')
    reviews = [obj.to_dict() for obj in (storage.all('Review')).values()
               if obj.place_id == place_id]
    return jsonify(reviews), 200


@app_views.route('/reviews/<string:review_id>', strict_slashes=False)
def get_review(review_id):
    """json data of a single review"""
    review = storage.get('Review', review_id)
    if review:
        return jsonify(review.to_dict()), 200
    abort(404)


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete data of a single review"""
    review = storage.get('Review', review_id)
    if review:
        review.delete()
        storage.save()
        return jsonify({})
    abort(404, 'Not found')


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates a new review"""
    dictionary = request.get_json()
    if dictionary is None:
        abort(400, 'Not a JSON')
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if dictionary.get('user_id') is None:
        abort(400, 'Missing user_id')
    user = storage.get('User', dictionary.get('user_id'))
    if user is None:
        abort(404)
    if dictionary.get('text') is None:
        abort(400, 'Missing text')
    dictionary['place_id'] = place_id
    review = Review(**dictionary)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update data of review"""
    dictionary = request.get_json()
    if dictionary is None:
        abort(400, 'Not a JSON')
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    [setattr(review, key, value) for key, value in dictionary.items()
     if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']]
    review.save()
    return jsonify(review.to_dict()), 200

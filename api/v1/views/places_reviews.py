#!/usr/bin/python3
"""place_reviews api handle for RESFUL API actions"""
from flask import abort, request, jsonify, make_response
from models import storage
from api.v1.views import app_views
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_place_reviews(place_id):
    """Get a place reviews"""
    place = storage.get('Place', place_id)
    print(place)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """Get a review by it id"""
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete form reviews table"""
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_place_review(place_id):
    """Post a review to a place"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    json_body = request.get_json()
    if not json_body:
        abort(400, 'Not a JSON')
    if 'user_id' not in json_body:
        abort(400, 'Missing user_id')
    user = storage.get('User', json_body['user_id'])
    if not user:
        abort(404)
    if 'text' not in json_body:
        abort(400, 'Missing text')
    json_body['place_id'] = place_id
    review = Review(**json_body)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update the review identified by the id"""
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    json_body = request.get_json()
    if not json_body:
        abort(400, "Not a JSON")
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, val in json_body.items():
        if key not in ignore_keys:
            setattr(review, key, val)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)

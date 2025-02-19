#!/usr/bin/python3
"""The places_reviews module"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Return all reviews of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def single_review(review_id):
    """Return a review based on its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    """Delete a review based on its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def push_review(place_id):
    """Add a new review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    new_review_req = request.get_json()
    if not new_review_req:
        abort(400, "Not a JSON")
    if 'user_id' not in new_review_req:
        abort(400, "Missing user_id")
    user_id = new_review_req['user_id']
    obj_user = storage.get(User, user_id)
    if not obj_user:
        abort(404)
    if 'text' not in new_review_req:
        abort(400, "Missing text")
    review = Review(**new_review_req)
    setattr(review, 'place_id', place_id)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Update an exist review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for key, value in req.items():
        if key not in ['id', 'user_id',
                       'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict())

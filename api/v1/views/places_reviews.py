#!/usr/bin/python3
"""route handlers for Review object"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage, storage_t
from models.review import Review
from models.place import Place


@app_views.route('/places/<place_id>/reviews')
def reviews_get(place_id):
    """
    get handler for reviews
    """
    place: Place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if storage_t == 'db':
        reviews = place.reviews
    else:
        reviews = place.reviews()

    reviews = [review.to_dict() for review in reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>')
def review_get(review_id):
    """
    get handler for review by id.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def review_delete(review_id):
    """
    route handler for deleting a review
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=["POST"])
def review_post(place_id):
    """
    route handler for creating a new review
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        return "Not a JSON", 400
    data = request.get_json()
    user_id = data.get('user_id')
    text = data.get('text')
    if not user_id:
        return "Missing user_id", 400
    if not text:
        return "Missing text", 400
    review = Review(user_id=user_id, text=text)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=["PUT"])
def review_put(review_id):
    """
    route handler for updating a review
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.is_json:
        return "Not a JSON", 400
    data = request.get_json()

    ignore = ('id', 'created_at', 'updated_at', 'user_id', 'place_id')

    for key, value in data.items():
        if key in ignore:
            continue
        else:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict())

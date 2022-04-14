#!/usr/bin/python3
"""
Api views for reviews
"""
from models.review import Review
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User
from models.place import Place


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_review(review_id):
    """
    Retrieve a review object
    """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Delete a review object
    """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Create a review object
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    if 'user_id' not in data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get("User", data['user_id'])
    if not user:
        abort(404)
    if 'text' not in data:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Update a review object
    """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for k, v in request.get_json().items():
        if k not in ['id', 'user_id', 'place_id',
                     'created_at', 'updated_at']:
            setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict())

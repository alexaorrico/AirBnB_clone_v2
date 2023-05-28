#!/usr/bin/python3
"""objects that handle all default RESTFul API actions"""
from models.review import Review
from models.user import User
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all review objects of a place"""
    place = storage.get(Place, place_id)
    ls_reviews = []
    if not place:
        abort(404)
    for review in place.reviews:
        ls_reviews.append(review.to_dict())
    return jsonify(ls_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrieves areview"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a specific review Object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Create a new review object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if 'text' not in data:
        abort(400, description="Missing text")

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Updates a specific review by id"""
    review = storage.get(Review, review_id)
    if review:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")

        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
    else:
        abort(404)

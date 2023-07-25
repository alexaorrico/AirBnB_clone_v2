#!/usr/bin/python3
"""
a new view for reviews objects
that handles all default RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews_of_place(place_id):
    """ retrives review objects of place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review_list = []
    for review in place.reviews:
        review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ retrieves a review object (specified with review_id) """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ deletes a review object (specified with review_id) """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Create a review object """
    data = request.get_json()
    place = storage.get(Place, place_id)
    user = storage.get(User, data.get("user_id"))
    if not place:
        abort(404)
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if not user:
        abort(404)
    if "text" not in data:
        abort(400, "Missing text")
    data["place_id"] = place_id
    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_reviews(review_id):
    """ updates a review object (specified with review_id) """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review_data = request.get_json()
    if not review_data:
        abort(400, "Not a JSON")
    for key, value in review_data.items():
        if key not in ('id', 'user_id', 'place_id',
                       'created_at', 'updated_at'):
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())

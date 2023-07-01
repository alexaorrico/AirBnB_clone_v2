#!/usr/bin/python3
"""module for the city file"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review
from models import storage


@app_views.route("/places/<place_id>/reviews", methods=['Get'], strict_slashes=False)
def retrieving_reviews(place_id):
    """retrieving the list of the reviews"""
    review_list = []
    check_place = storage.get("Place", place_id)
    if check_place is None:
        abort(404)
    reviews = storage.all("Reviews")
    for review in reviews.values():
        if place_id == getattr(review, "place_id"):
            review_list.append(review.to_dict())
    return jsonify(review_list), 200


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def retrieve_review(review_id):
    """retrieving the review id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/review_id>", methods=['DELETE'], strict_slashes=False)
def deleting_review(review_id):
    """deleting a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", mehtods=['POST'], strict_slashes=False)
def creating_review(place_id):
    """creating a review"""
    post_data = request.get_json()
    if post_data is None:
        abort(400, 'Not a JSON')
    if post_data.get('user_id') is None:
        abort(400, 'Missing user_id')
    if post_data.get('text') is None:
        abort(400, 'Missing text')
    check_state = storage.get("Place", place_id)
    if check_state is None:
        abort(404)
    check_state = storage.get("User", post_data.get('user_id'))
    if check_state is None:
        abort(404)
    post_data['place_id'] = place_id
    new_review = Review(**post_data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """updating the review"""
    keys_ignored = ['id', 'created_at', 'updated_at',
                    'user_id', 'place_id', 'state_id']
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    put_data = request.get_json()
    if put_data is None:
        abort(404, "Not a JSON")
    for key, value in put_data.items():
        if key in keys_ignored:
            pass
        else:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200

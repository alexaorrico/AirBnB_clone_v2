#!/usr/bin/python3
""" for places and amenities view """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.city import City
from models.state import State
from models.review import Review
from models.place import Place
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def getAllReviews(place_id):
    """Retrieves list of review objects of place """
    review_list = []
    all_reviews = storage.all('Review')

    get_place = storage.get("Place", place_id)
    if get_place is None:
        abort(404)

    for item in all_reviews.values():
        if item.place_id == place_id:
            review_list.append(item.to_dict())

    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def getReview(review_id):
    """return review object matching review_id """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def DEL_review(review_id):
    """delete a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def POST_review(place_id):
    """adds a review"""
    post_content = request.get_json()

    if not request.is_json:
        abort(400, "Not a JSON")

    user_id = post_content.get('user_id')
    if not user_id:
        abort(400, "Missing user_id")

    text = post_content.get('text')
    if not text:
        abort(400, "Missing text")

    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    new_review = Review(**post_content)
    new_review.place_id = place_id
    storage.new(new_review)
    new_review.save()
    storage.close()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def PUT_review(review_id):
    """updates review object"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    update_content = request.get_json()
    if not request.is_json:
        abort(400, "Not a JSON")

    ignore_keys = ["id", "place_id", "user_id", "created_at", "updated_at"]

    for key, val in update_content.items():
        if key not in ignore_keys:
            setattr(review, key, val)
    review.save()
    storage.close()
    return jsonify(review.to_dict()), 200

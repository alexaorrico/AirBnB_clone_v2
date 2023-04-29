#!/usr/bin/python3
"""This view implements RESTful API operations for `Review` objects"""
from flask import jsonify, abort, request, make_response
from . import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def read_reviews(place_id):
    """Retrieves a list of `Review` objects associated with given `place_id`"""

    if storage.get(Place, place_id) is None:
        abort(404)

    return jsonify([
        review.to_dict() for review in storage.all(Review).values()
        if review.place_id == place_id
    ])


@app_views.route('/reviews/<review_id>', methods=['GET'])
def read_review(review_id):
    """Retrieves a `Review` object associated with given `review_id`"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a `Review` object associated with given `review_id`"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Creates a `Review` object associated with given `place_id`"""

    if storage.get(Place, place_id) is None:
        abort(404)

    review_data = request.get_json(silent=True)
    if not review_data:
        abort(400, "Not a JSON")

    if "user_id" not in review_data:
        abort(400, "Missing user_id")

    user_id = review_data["user_id"]
    if storage.get(User, user_id) is None:
        abort(404)

    if "text" not in review_data:
        abort(400, "Missing text")

    new_review = Review(place_id=place_id, user_id=user_id,
                        text=review_data["text"])

    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a `Review` object associated with given `review_id`"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review_data = request.get_json(silent=True)
    if not review_data:
        abort(400, "Not a JSON")

    allowed = ("text")
    for key, value in review_data.items():
        if key in allowed:
            setattr(review, key, value)

    review.save()
    return make_response(jsonify(review.to_dict()), 200)

#!/usr/bin/python3

"""
create new view for Review objects
that handles all default RESTFul API actions
    - retrive a list of Review object by place id
    - retrive a Review object
    - delete a Review object
    - create a new Review object
    - update a Review object
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_by_place(place_id):
    """
    Retrieves the list of all Review objects of a place
    using the place_id
    """
    if place_id is not None:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        reviewList = [review.to_dict() for review in place.reviews]
        return jsonify(reviewList)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_by_id(review_id):
    """
    Retrieves a Review object by the review_id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object by the review_id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review object using place_id
    """
    user_id = request.get_json().get('user_id')

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "user_id" not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    elif "text" not in request.get_json():
        return jsonify({"error": "Missing text"}), 400
    elif storage.get(User, user_id) is None:
        abort(404)
    else:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        new_review = Review()
        new_review.place_id = place_id
        new_review.user_id = request.get_json().get('user_id')
        new_review.text = request.get_json().get('text')
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    update a Review object using review_id
    """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.text = request.get_json().get('text')
    review.save()
    return jsonify(review.to_dict())

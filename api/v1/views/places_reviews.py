#!/usr/bin/python3
""" Blueprint for Review objs that handles all default RestFul API actions """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=["GET"], strict_slashes=False)
def list_places_by_review(place_id):
    """list places by review"""
    place_object = storage.get("Place", place_id)
    if not place_object:
        abort(404)
    my_reviews = [review.to_dict() for review in place_object.reviews]
    return (jsonify(my_reviews), 200)


@app_views.route('/reviews/<review_id>', methods=["GET"], strict_slashes=False)
def review(review_id):
    """ Retrieves Review obj """
    my_review = storage.get("Review", review_id)
    if my_review is None:
        abort(404)
    return (jsonify(my_review.to_dict()), 200)


@app_views.route('/reviews/<review_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_reviews(review_id):
    """ Deletes a Review obj based on its' id """

    my_review = storage.get("Review", review_id)
    if my_review is None:
        abort(404)
    storage.delete(my_review)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=["POST"], strict_slashes=False)
def reviews_by_place(place_id=None):
    """gets the reviews by place"""
    content = request.get_json()
    my_place = storage.get("Place", place_id)
    if my_place is None:
        abort(404)
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    my_name = content.get("name")
    if my_name is None:
        return (jsonify({"error": "Missing name"}), 400)
    new_review = Review(**content)
    new_review.state_id = place_id
    new_review.save()

    return(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=["POST"], strict_slashes=False)
@app_views.route('/reviews', methods=["POST"], strict_slashes=False)
def post_reviews(review_id=None):
    """ Creates a Review """
    content = request.get_json()
    my_review = storage.get("Review", review_id)
    if my_review is None:
        abort(404)
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    name = content.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    new_review = Review(**content)
    new_review.save()

    return (jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=["PUT"], strict_slashes=False)
def update_reviews(review_id):
    """ Updates a Review obj & id """
    content = request.get_json()
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    my_review = storage.get("Review", review_id)
    if my_review is None:
        abort(404)

    not_allowed = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in content.items():
        if key not in not_allowed:
            setattr(my_review, key, value)

    my_review.save()
    return (jsonify(my_review.to_dict()), 200)
